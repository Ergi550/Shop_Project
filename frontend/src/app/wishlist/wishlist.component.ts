import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LayoutComponent } from '../layout/layout.component';
import { WishlistService } from '../core/services/wishlist.service';

@Component({
  selector: 'app-wishlist',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './wishlist.component.html',
})
export class WishlistComponent {
  wishlist = inject(WishlistService);

  private movingIds = signal<Set<number>>(new Set());

  items = this.wishlist.items;
  itemCount = this.wishlist.itemCount;

  isMoving(productId: number): boolean {
    return this.movingIds().has(productId);
  }

  moveToCart(productId: number): void {
    this.movingIds.update(ids => new Set([...ids, productId]));
    setTimeout(() => {
      this.wishlist.removeItem(productId);
      this.movingIds.update(ids => { ids.delete(productId); return new Set(ids); });
    }, 800);
  }

  remove(productId: number): void {
    this.wishlist.removeItem(productId);
  }
}
