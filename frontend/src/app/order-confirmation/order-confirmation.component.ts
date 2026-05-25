import { Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';
import { OrderService } from '../core/services/order.service';

interface DisplayItem {
  name: string;
  size: string;
  color: string;
  price: number;
  quantity: number;
  imageUrl: string;
}

const FALLBACK_ITEMS: DisplayItem[] = [
  {
    name: 'Silk Midi Dress', size: 'S', color: 'Ivory', price: 385, quantity: 1,
    imageUrl: 'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=200',
  },
  {
    name: 'Leather Kitten Heels', size: '38', color: 'Noir', price: 310, quantity: 1,
    imageUrl: 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=200',
  },
  {
    name: 'Pearl Drop Earrings', size: 'One Size', color: 'Pearl White', price: 145, quantity: 2,
    imageUrl: 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=200',
  },
];

@Component({
  selector: 'app-order-confirmation',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './order-confirmation.component.html',
})
export class OrderConfirmationComponent {
  private orderService = inject(OrderService);

  private realOrder = this.orderService.lastOrder;

  orderNumber = computed(() => {
    const o = this.realOrder();
    return o ? `AUR-${o.id.toString().padStart(6, '0')}` : 'AUR-20260525-4817';
  });

  estimatedDelivery = 'In 3–5 business days';

  shippingAddress = computed(() => {
    const o = this.realOrder();
    return o
      ? { name: o.shipping_full_name, address: o.shipping_address, city: o.shipping_city, postcode: o.shipping_postcode, country: o.shipping_country }
      : { name: 'Ergi Duka', address: 'Rruga e Durrësit 14', city: 'Tirana', postcode: '1001', country: 'Albania' };
  });

  orderItems = computed<DisplayItem[]>(() => FALLBACK_ITEMS);

  subtotal = computed(() => this.orderItems().reduce((s, i) => s + i.price * i.quantity, 0));
  shipping = 0;
  total = computed(() => this.realOrder()?.total ?? this.subtotal());
}
