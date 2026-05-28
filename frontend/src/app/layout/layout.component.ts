import { Component, HostListener, Input, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CartService } from '../core/services/cart.service';
import { AuthService } from '../core/services/auth.service';

interface NavCategory {
  name: string;
  slug: string;
}

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './layout.component.html',
})
export class LayoutComponent {
  @Input() solidNav = false;

  cart = inject(CartService);
  auth = inject(AuthService);

  scrolled = signal(false);
  menuOpen = signal(false);
  searchOpen = signal(false);
  accountOpen = signal(false);

  categories: NavCategory[] = [
    { name: 'New Arrivals', slug: 'new-arrivals' },
    { name: 'Dresses', slug: 'dresses' },
    { name: 'Tops', slug: 'tops' },
    { name: 'Shoes', slug: 'shoes' },
    { name: 'Accessories', slug: 'accessories' },
    { name: 'Sale', slug: 'sale' },
  ];

  @HostListener('window:scroll')
  onWindowScroll(): void {
    this.scrolled.set(window.scrollY > 50);
  }

  openMenu(): void {
    this.menuOpen.set(true);
    this.searchOpen.set(false);
    this.accountOpen.set(false);
  }

  closeMenu(): void {
    this.menuOpen.set(false);
  }

  openSearch(): void {
    this.searchOpen.set(true);
    this.menuOpen.set(false);
    this.accountOpen.set(false);
  }

  closeSearch(): void {
    this.searchOpen.set(false);
  }

  toggleAccount(): void {
    this.accountOpen.update(v => !v);
    this.menuOpen.set(false);
    this.searchOpen.set(false);
  }

  closeAccount(): void {
    this.accountOpen.set(false);
  }

  get navDark(): boolean {
    return this.solidNav || this.scrolled() || this.menuOpen() || this.searchOpen();
  }
}
