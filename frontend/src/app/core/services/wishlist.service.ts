import { Injectable, signal, computed } from '@angular/core';
import { WishlistItem } from '../models';

@Injectable({ providedIn: 'root' })
export class WishlistService {
  private userId: string | null = null;
  private _items = signal<WishlistItem[]>([]);

  readonly items = this._items.asReadonly();
  readonly itemCount = computed(() => this._items().length);

  addItem(item: WishlistItem): void {
    if (this.has(item.productId)) return;
    this._items.update(items => [...items, item]);
    this.save();
  }

  removeItem(productId: number): void {
    this._items.update(items => items.filter(i => i.productId !== productId));
    this.save();
  }

  toggle(item: WishlistItem): void {
    this.has(item.productId) ? this.removeItem(item.productId) : this.addItem(item);
  }

  has(productId: number): boolean {
    return this._items().some(i => i.productId === productId);
  }

  switchUser(userId: string | null): void {
    this.userId = userId;
    this._items.set(this.load());
  }

  clear(): void {
    this._items.set([]);
    localStorage.removeItem(this.key);
  }

  private get key(): string {
    return `aurelia_wishlist_${this.userId ?? 'guest'}`;
  }

  private save(): void {
    localStorage.setItem(this.key, JSON.stringify(this._items()));
  }

  private load(): WishlistItem[] {
    try {
      const raw = localStorage.getItem(this.key);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }
}
