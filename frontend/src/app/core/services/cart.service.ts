import { Injectable, signal, computed } from '@angular/core';
import { CartItem } from '../models';

const STORAGE_KEY = 'aurelia_cart';

@Injectable({ providedIn: 'root' })
export class CartService {
  private _items = signal<CartItem[]>(this.load());

  readonly items = this._items.asReadonly();

  readonly itemCount = computed(() =>
    this._items().reduce((sum, i) => sum + i.quantity, 0)
  );

  readonly subtotal = computed(() =>
    this._items().reduce((sum, i) => sum + i.price * i.quantity, 0)
  );

  readonly shipping = computed(() =>
    this.subtotal() >= 250 ? 0 : 12
  );

  readonly total = computed(() => this.subtotal() + this.shipping());

  addItem(item: CartItem): void {
    this._items.update(items => {
      const existing = items.find(
        i => i.variantId === item.variantId
      );
      if (existing) {
        return items.map(i =>
          i.variantId === item.variantId
            ? { ...i, quantity: i.quantity + item.quantity }
            : i
        );
      }
      return [...items, item];
    });
    this.save();
  }

  updateQuantity(variantId: number, quantity: number): void {
    if (quantity < 1) { this.removeItem(variantId); return; }
    this._items.update(items =>
      items.map(i => i.variantId === variantId ? { ...i, quantity } : i)
    );
    this.save();
  }

  removeItem(variantId: number): void {
    this._items.update(items => items.filter(i => i.variantId !== variantId));
    this.save();
  }

  clear(): void {
    this._items.set([]);
    localStorage.removeItem(STORAGE_KEY);
  }

  private save(): void {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this._items()));
  }

  private load(): CartItem[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }
}
