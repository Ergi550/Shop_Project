import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { LayoutComponent } from '../layout/layout.component';
import { AuthService } from '../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule, LayoutComponent],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  email = signal('');
  password = signal('');
  showPassword = signal(false);
  submitted = signal(false);
  loading = signal(false);
  error = signal('');

  submit(): void {
    if (!this.email() || !this.password()) {
      this.error.set('Please enter your email and password.');
      return;
    }
    this.loading.set(true);
    this.error.set('');
    this.auth.login(this.email(), this.password()).subscribe({
      next: (user) => {
        this.loading.set(false);
        if (user.is_staff) {
          this.router.navigate(['/admin']);
        } else {
          this.submitted.set(true);
          setTimeout(() => this.router.navigate(['/']), 1500);
        }
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Invalid email or password.');
      },
    });
  }
}
