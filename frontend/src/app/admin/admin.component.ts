import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../core/services/auth.service';

interface NavItem {
  label: string;
  path: string;
  icon: string;
}

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './admin.component.html',
})
export class AdminComponent {
  auth = inject(AuthService);
  private router = inject(Router);

  sidebarOpen = signal(false);

  navItems: NavItem[] = [
    { label: 'Dashboard',  path: '/admin/dashboard',   icon: 'dashboard' },
    { label: 'Products',   path: '/admin/products',    icon: 'products'  },
    { label: 'Categories', path: '/admin/categories',  icon: 'categories'},
    { label: 'Orders',     path: '/admin/orders',      icon: 'orders'    },
  ];

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
