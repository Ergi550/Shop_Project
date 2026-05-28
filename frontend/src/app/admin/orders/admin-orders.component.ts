import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../admin.service';
import { AdminOrderSummary, AdminOrderDetail } from '../admin-models';

const STATUSES = ['pending', 'paid', 'shipped', 'delivered', 'cancelled'] as const;

@Component({
  selector: 'app-admin-orders',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-orders.component.html',
})
export class AdminOrdersComponent implements OnInit {
  private svc = inject(AdminService);

  statuses = STATUSES;
  activeFilter = signal('');
  orders = signal<AdminOrderSummary[]>([]);
  loading = signal(true);
  error = signal('');

  // Detail panel
  detailOpen = signal(false);
  detail = signal<AdminOrderDetail | null>(null);
  detailLoading = signal(false);
  selectedStatus = signal('');
  statusSaving = signal(false);
  statusError = signal('');

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading.set(true);
    this.svc.getOrders(this.activeFilter() || undefined).subscribe({
      next: o => { this.orders.set(o); this.loading.set(false); },
      error: () => { this.error.set('Failed to load orders.'); this.loading.set(false); },
    });
  }

  setFilter(status: string): void {
    this.activeFilter.set(status);
    this.load();
  }

  openDetail(id: number): void {
    this.detailOpen.set(true);
    this.detailLoading.set(true);
    this.statusError.set('');
    this.svc.getOrder(id).subscribe({
      next: d => {
        this.detail.set(d);
        this.selectedStatus.set(d.status);
        this.detailLoading.set(false);
      },
      error: () => { this.detailLoading.set(false); },
    });
  }

  closeDetail(): void { this.detailOpen.set(false); this.detail.set(null); }

  saveStatus(): void {
    const d = this.detail();
    if (!d) return;
    this.statusSaving.set(true);
    this.statusError.set('');
    this.svc.updateOrderStatus(d.id, this.selectedStatus()).subscribe({
      next: updated => {
        this.detail.set(updated);
        this.statusSaving.set(false);
        // Refresh list row
        this.orders.update(list =>
          list.map(o => o.id === updated.id ? { ...o, status: updated.status } : o)
        );
      },
      error: () => { this.statusError.set('Failed to update status.'); this.statusSaving.set(false); },
    });
  }

  statusColor(status: string): string {
    const map: Record<string, string> = {
      pending:   'text-yellow-700 bg-yellow-50 border-yellow-200',
      paid:      'text-blue-700 bg-blue-50 border-blue-200',
      shipped:   'text-purple-700 bg-purple-50 border-purple-200',
      delivered: 'text-green-700 bg-green-50 border-green-200',
      cancelled: 'text-red-600 bg-red-50 border-red-200',
    };
    return map[status] ?? 'text-gray-500 bg-gray-50 border-gray-200';
  }

  customerName(d: AdminOrderDetail): string {
    const n = `${d.customer.first_name} ${d.customer.last_name}`.trim();
    return n || d.customer.username;
  }
}
