import { Injectable, signal, computed } from '@angular/core';
import { WishlistItem } from '../models';

const STORAGE_KEY = 'aurelia_wishlist';

@Injectable({ providedIn: 'root' })
export class WishlistService {
  private _items = signal<WishlistItem[]>(this.load());

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

  clear(): void {
    this._items.set([]);
    localStorage.removeItem(STORAGE_KEY);
  }

  private save(): void {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this._items()));
  }

  private load(): WishlistItem[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }
}
