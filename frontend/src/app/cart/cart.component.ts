import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';
import { CartService } from '../core/services/cart.service';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './cart.component.html',
})
export class CartComponent {
  cart = inject(CartService);

  get items() { return this.cart.items; }
  get itemCount() { return this.cart.itemCount; }
  get subtotal() { return this.cart.subtotal; }
  get shipping() { return this.cart.shipping; }
  get total() { return this.cart.total; }

  increment(variantId: number): void {
    const item = this.cart.items().find(i => i.variantId === variantId);
    if (item) this.cart.updateQuantity(variantId, item.quantity + 1);
  }

  decrement(variantId: number): void {
    const item = this.cart.items().find(i => i.variantId === variantId);
    if (item) this.cart.updateQuantity(variantId, item.quantity - 1);
  }

  remove(variantId: number): void {
    this.cart.removeItem(variantId);
  }
}
