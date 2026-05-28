import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AdminService } from '../admin.service';
import { AdminDashboard } from '../admin-models';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './admin-dashboard.component.html',
})
export class AdminDashboardComponent implements OnInit {
  private svc = inject(AdminService);

  data = signal<AdminDashboard | null>(null);
  loading = signal(true);
  error = signal('');

  ngOnInit(): void {
    this.svc.getDashboard().subscribe({
      next: d => { this.data.set(d); this.loading.set(false); },
      error: () => { this.error.set('Failed to load dashboard.'); this.loading.set(false); },
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

  stockColor(stock: number): string {
    if (stock === 0) return 'text-red-600 font-semibold';
    if (stock <= 2) return 'text-red-500';
    return 'text-yellow-600';
  }
}
