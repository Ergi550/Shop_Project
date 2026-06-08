import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
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
  private router = inject(Router);

  items = this.wishlist.items;
  itemCount = this.wishlist.itemCount;

  moveToCart(slug: string): void {
    this.router.navigate(['/product', slug], { queryParams: { from: 'wishlist' } });
  }

  remove(productId: number): void {
    this.wishlist.removeItem(productId);
  }
}
