import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  AdminDashboard, AdminCategory, AdminProductSummary, AdminProductDetail,
  AdminVariant, AdminOrderSummary, AdminOrderDetail,
} from './admin-models';

@Injectable({ providedIn: 'root' })
export class AdminService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/admin`;

  // Dashboard
  getDashboard(): Observable<AdminDashboard> {
    return this.http.get<AdminDashboard>(`${this.base}/dashboard/`);
  }

  // Categories
  getCategories(): Observable<AdminCategory[]> {
    return this.http.get<AdminCategory[]>(`${this.base}/categories/`);
  }
  createCategory(data: Partial<AdminCategory>): Observable<AdminCategory> {
    return this.http.post<AdminCategory>(`${this.base}/categories/`, data);
  }
  updateCategory(id: number, data: Partial<AdminCategory>): Observable<AdminCategory> {
    return this.http.patch<AdminCategory>(`${this.base}/categories/${id}/`, data);
  }
  deleteCategory(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/categories/${id}/`);
  }

  // Products
  getProducts(search?: string): Observable<AdminProductSummary[]> {
    let params = new HttpParams();
    if (search) params = params.set('search', search);
    return this.http.get<AdminProductSummary[]>(`${this.base}/products/`, { params });
  }
  getProduct(id: number): Observable<AdminProductDetail> {
    return this.http.get<AdminProductDetail>(`${this.base}/products/${id}/`);
  }
  createProduct(data: FormData): Observable<AdminProductDetail> {
    return this.http.post<AdminProductDetail>(`${this.base}/products/`, data);
  }
  updateProduct(id: number, data: FormData): Observable<AdminProductDetail> {
    return this.http.patch<AdminProductDetail>(`${this.base}/products/${id}/`, data);
  }
  deleteProduct(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/products/${id}/`);
  }

  // Variants
  createVariant(productId: number, data: Omit<AdminVariant, 'id'>): Observable<AdminVariant> {
    return this.http.post<AdminVariant>(`${this.base}/products/${productId}/variants/`, data);
  }
  updateVariant(id: number, data: Partial<Omit<AdminVariant, 'id'>>): Observable<AdminVariant> {
    return this.http.patch<AdminVariant>(`${this.base}/variants/${id}/`, data);
  }
  deleteVariant(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/variants/${id}/`);
  }

  // Orders
  getOrders(status?: string): Observable<AdminOrderSummary[]> {
    let params = new HttpParams();
    if (status) params = params.set('status', status);
    return this.http.get<AdminOrderSummary[]>(`${this.base}/orders/`, { params });
  }
  getOrder(id: number): Observable<AdminOrderDetail> {
    return this.http.get<AdminOrderDetail>(`${this.base}/orders/${id}/`);
  }
  updateOrderStatus(id: number, status: string): Observable<AdminOrderDetail> {
    return this.http.patch<AdminOrderDetail>(`${this.base}/orders/${id}/status/`, { status });
  }
}
