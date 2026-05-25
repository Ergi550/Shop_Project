import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { LayoutComponent } from '../layout/layout.component';
import { CartService } from '../core/services/cart.service';
import { OrderService } from '../core/services/order.service';

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule, LayoutComponent],
  templateUrl: './checkout.component.html',
})
export class CheckoutComponent {
  private cartService = inject(CartService);
  private orderService = inject(OrderService);
  private router = inject(Router);

  step = signal<'shipping' | 'payment'>('shipping');
  loading = signal(false);
  error = signal('');

  form = signal({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    postcode: '',
    country: '',
  });

  get orderItems() { return this.cartService.items; }
  get subtotal() { return this.cartService.subtotal; }
  get shipping() { return this.cartService.shipping; }
  get total() { return this.cartService.total; }

  countries = [
    'Albania', 'Austria', 'Belgium', 'Croatia', 'Czech Republic',
    'Denmark', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
    'Ireland', 'Italy', 'Kosovo', 'Netherlands', 'Norway', 'Poland',
    'Portugal', 'Romania', 'Spain', 'Sweden', 'Switzerland',
    'United Kingdom', 'United States',
  ];

  updateField(field: string, value: string): void {
    this.form.update(f => ({ ...f, [field]: value }));
  }

  proceedToPayment(): void {
    this.step.set('payment');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  backToShipping(): void {
    this.step.set('shipping');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  placeOrder(): void {
    const f = this.form();
    const items = this.cartService.items();
    if (!items.length) return;

    this.loading.set(true);
    this.error.set('');

    this.orderService.createOrder({
      shipping_full_name: `${f.firstName} ${f.lastName}`.trim(),
      shipping_address: f.address,
      shipping_city: f.city,
      shipping_postcode: f.postcode,
      shipping_country: f.country,
      shipping_phone: f.phone,
      items: items.map(i => ({ variant: i.variantId, quantity: i.quantity })),
    }).subscribe({
      next: () => {
        this.cartService.clear();
        this.loading.set(false);
        this.router.navigate(['/order-confirmation']);
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Could not place order. Please try again.');
      },
    });
  }
}
