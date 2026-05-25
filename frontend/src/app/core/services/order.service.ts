import { Injectable, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Order, OrderCreatePayload } from '../models';

@Injectable({ providedIn: 'root' })
export class OrderService {
  private http = inject(HttpClient);
  private api = environment.apiUrl;

  private _lastOrder = signal<Order | null>(null);
  readonly lastOrder = this._lastOrder.asReadonly();

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.api}/orders/`);
  }

  createOrder(payload: OrderCreatePayload): Observable<Order> {
    return this.http.post<Order>(`${this.api}/orders/create/`, payload).pipe(
      tap(order => this._lastOrder.set(order))
    );
  }
}
