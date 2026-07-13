import { Component, inject, signal, computed, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';
import { AuthService } from '../core/services/auth.service';

@Component({
  selector: 'app-verify-email',
  standalone: true,
  imports: [RouterLink, LayoutComponent],
  templateUrl: './verify-email.component.html',
})
export class VerifyEmailComponent implements OnInit, OnDestroy {
  private route  = inject(ActivatedRoute);
  private router = inject(Router);
  private auth   = inject(AuthService);

  email   = signal('');
  digits  = signal<string[]>(['', '', '', '', '', '']);
  code    = computed(() => this.digits().join(''));

  loading  = signal(false);
  verified = signal(false);
  error    = signal('');

  resendLoading  = signal(false);
  resendCooldown = signal(0);
  private cooldownTimer?: ReturnType<typeof setInterval>;

  ngOnInit(): void {
    const email = this.route.snapshot.queryParamMap.get('email') ?? '';
    this.email.set(email);
  }

  ngOnDestroy(): void {
    if (this.cooldownTimer) clearInterval(this.cooldownTimer);
  }

  onDigitInput(event: Event, index: number): void {
    const input = event.target as HTMLInputElement;
    const raw   = input.value.replace(/\D/g, '');
    const digit = raw.slice(-1);

    const next = [...this.digits()];
    next[index] = digit;
    this.digits.set(next);
    this.error.set('');

    if (digit && index < 5) {
      document.getElementById(`digit-${index + 1}`)?.focus();
    }
  }

  onDigitKeydown(event: KeyboardEvent, index: number): void {
    if (event.key === 'Backspace') {
      const next = [...this.digits()];
      if (next[index]) {
        next[index] = '';
        this.digits.set(next);
      } else if (index > 0) {
        document.getElementById(`digit-${index - 1}`)?.focus();
      }
    }
  }

  onPaste(event: ClipboardEvent): void {
    event.preventDefault();
    const text   = event.clipboardData?.getData('text') ?? '';
    const digits = text.replace(/\D/g, '').slice(0, 6).split('');
    const next   = ['', '', '', '', '', ''];
    digits.forEach((d, i) => { next[i] = d; });
    this.digits.set(next);
    const focusIdx = Math.min(digits.length, 5);
    document.getElementById(`digit-${focusIdx}`)?.focus();
  }

  submit(): void {
    if (this.code().length < 6) {
      this.error.set('Please enter the full 6-digit code.');
      return;
    }
    this.loading.set(true);
    this.error.set('');

    this.auth.verifyEmail(this.email(), this.code()).subscribe({
      next: () => {
        this.loading.set(false);
        this.verified.set(true);
        setTimeout(() => this.router.navigate(['/login']), 2500);
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err?.error?.detail ?? 'Verification failed. Please try again.');
        this.digits.set(['', '', '', '', '', '']);
        setTimeout(() => document.getElementById('digit-0')?.focus(), 50);
      },
    });
  }

  resend(): void {
    if (this.resendCooldown() > 0 || this.resendLoading()) return;
    this.resendLoading.set(true);
    this.error.set('');

    this.auth.resendCode(this.email()).subscribe({
      next: () => {
        this.resendLoading.set(false);
        this.startCooldown();
        this.digits.set(['', '', '', '', '', '']);
        setTimeout(() => document.getElementById('digit-0')?.focus(), 50);
      },
      error: (err) => {
        this.resendLoading.set(false);
        this.error.set(err?.error?.detail ?? 'Could not resend code. Please try again.');
      },
    });
  }

  private startCooldown(): void {
    this.resendCooldown.set(30);
    this.cooldownTimer = setInterval(() => {
      this.resendCooldown.update(v => {
        if (v <= 1) { clearInterval(this.cooldownTimer); return 0; }
        return v - 1;
      });
    }, 1000);
  }
}
