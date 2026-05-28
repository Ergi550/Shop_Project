import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthUser } from '../models';
import { CartService } from './cart.service';
import { WishlistService } from './wishlist.service';
import { OrderService } from './order.service';

interface TokenResponse {
  access: string;
  refresh: string;
}

interface RegisterPayload {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private cart = inject(CartService);
  private wishlist = inject(WishlistService);
  private orders = inject(OrderService);
  private api = environment.apiUrl;

  private _user = signal<AuthUser | null>(this.loadUser());
  readonly currentUser = this._user.asReadonly();
  readonly isLoggedIn = computed(() => this._user() !== null);

  constructor() {
    const user = this._user();
    if (user) {
      this.cart.switchUser(String(user.id));
      this.wishlist.switchUser(String(user.id));
    }
  }

  login(email: string, password: string): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${this.api}/auth/token/`, { username: email, password }).pipe(
      tap(tokens => {
        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
        this.fetchMe();
      })
    );
  }

  register(payload: RegisterPayload): Observable<AuthUser> {
    return this.http.post<AuthUser>(`${this.api}/auth/register/`, {
      ...payload,
      username: payload.email,
    });
  }

  fetchMe(): void {
    this.http.get<AuthUser>(`${this.api}/auth/me/`).subscribe({
      next: user => {
        this._user.set(user);
        localStorage.setItem('auth_user', JSON.stringify(user));
        this.cart.switchUser(String(user.id));
        this.wishlist.switchUser(String(user.id));
      },
      error: () => this.logout(),
    });
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('auth_user');
    this._user.set(null);
    this.cart.switchUser(null);
    this.wishlist.switchUser(null);
    this.orders.clearLastOrder();
  }

  private loadUser(): AuthUser | null {
    try {
      const raw = localStorage.getItem('auth_user');
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }
}
