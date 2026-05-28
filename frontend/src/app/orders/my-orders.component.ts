import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';
import { OrderService } from '../core/services/order.service';
import { Order } from '../core/models';

@Component({
  selector: 'app-my-orders',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './my-orders.component.html',
})
export class MyOrdersComponent implements OnInit {
  private orderService = inject(OrderService);

  orders = signal<Order[]>([]);
  loading = signal(true);
  error = signal('');
  expandedOrderId = signal<number | null>(null);

  ngOnInit(): void {
    this.orderService.getOrders().subscribe({
      next: (orders) => {
        this.orders.set(orders);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Could not load your orders. Please try again.');
        this.loading.set(false);
      },
    });
  }

  toggleOrder(id: number): void {
    this.expandedOrderId.set(this.expandedOrderId() === id ? null : id);
  }

  statusColor(status: string): string {
    const map: Record<string, string> = {
      pending: 'text-yellow-600 bg-yellow-50',
      paid: 'text-blue-600 bg-blue-50',
      shipped: 'text-purple-600 bg-purple-50',
      delivered: 'text-green-600 bg-green-50',
      cancelled: 'text-red-500 bg-red-50',
    };
    return map[status] ?? 'text-gray-500 bg-gray-50';
  }
}
