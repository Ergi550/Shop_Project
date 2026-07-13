import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { LayoutComponent } from '../layout/layout.component';
import { AuthService } from '../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule, LayoutComponent],
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  firstName = signal('');
  lastName = signal('');
  email = signal('');
  password = signal('');
  confirmPassword = signal('');
  showPassword = signal(false);
  acceptsMarketing = signal(false);
  submitted = signal(false);
  loading = signal(false);
  error = signal('');

  submit(): void {
    if (!this.email() || !this.password()) {
      this.error.set('Please fill in all required fields.');
      return;
    }
    if (this.password() !== this.confirmPassword()) {
      this.error.set('Passwords do not match.');
      return;
    }
    if (this.password().length < 8) {
      this.error.set('Password must be at least 8 characters.');
      return;
    }
    this.loading.set(true);
    this.error.set('');
    this.auth.register({
      email: this.email(),
      password: this.password(),
      first_name: this.firstName(),
      last_name: this.lastName(),
    }).subscribe({
      next: () => {
        this.loading.set(false);
        this.router.navigate(['/verify-email'], { queryParams: { email: this.email() } });
      },
      error: (err) => {
        this.loading.set(false);
        this.error.set(err?.error?.detail ?? 'Registration failed. Please try again.');
      },
    });
  }
}
