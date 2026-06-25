import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal, toObservable } from '@angular/core/rxjs-interop';
import { switchMap, catchError, of, map } from 'rxjs';
import { LayoutComponent } from '../layout/layout.component';
import { ProductService } from '../core/services/product.service';
import { CartService } from '../core/services/cart.service';
import { WishlistService } from '../core/services/wishlist.service';
import { Product } from '../core/models';
import { productImages, getColorHex, PLACEHOLDER_IMAGE } from '../core/product-images';
import { SizeGuideService } from '../core/services/size-guide.service';

interface DisplayColor {
  name: string;
  hex: string;
}

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './product-detail.component.html',
})
export class ProductDetailComponent {
  private route = inject(ActivatedRoute);
  private productService = inject(ProductService);
  private cartService = inject(CartService);
  private wishlistService = inject(WishlistService);
  sizeGuide = inject(SizeGuideService);

  private slug = toSignal(
    this.route.paramMap.pipe(map(p => p.get('slug') ?? '')),
    { initialValue: '' }
  );

  readonly fromWishlist = toSignal(
    this.route.queryParamMap.pipe(map(q => q.get('from') === 'wishlist')),
    { initialValue: false }
  );
  wishlistPopupDismissed = signal(false);

  private productRaw = toSignal<Product | null>(
    toObservable(this.slug).pipe(
      switchMap(slug =>
        slug ? this.productService.getProduct(slug).pipe(catchError(() => of(null))) : of(null)
      )
    )
  );

  readonly loading = computed(() => this.productRaw() === undefined);
  readonly product = computed(() => this.productRaw() ?? null);

  activeImageIndex = signal(0);
  selectedSize = signal<string | null>(null);
  selectedColor = signal<string | null>(null);
  quantity = signal(1);
  activeTab = signal<'description' | 'materials' | 'care'>('description');
  addedToCart = signal(false);
  addedToWishlist = signal(false);
  sizeError = signal(false);
  colorError = signal(false);

  images = computed(() => {
    const p = this.product();
    if (!p) return [PLACEHOLDER_IMAGE];
    return productImages(p.slug, p.image);
  });

  activeImage = computed(() => this.images()[this.activeImageIndex()]);

  sizes = computed<string[]>(() => {
    const p = this.product();
    if (!p) return [];
    return [...new Set(p.variants.map(v => v.size.trim()).filter(s => s.length > 0))];
  });

  colors = computed<DisplayColor[]>(() => {
    const p = this.product();
    if (!p) return [];
    const unique = [...new Set(p.variants.map(v => v.color.trim()).filter(c => c.length > 0))];
    return unique.map(name => ({ name, hex: getColorHex(name) }));
  });

  isInWishlist = computed(() => {
    const p = this.product();
    return p ? this.wishlistService.has(p.id) : false;
  });

  isSizeAvailable(size: string): boolean {
    const p = this.product();
    if (!p) return false;
    const color = this.selectedColor();
    if (!color) return p.variants.some(v => v.size.trim() === size && v.stock > 0);
    return p.variants.some(v => v.size.trim() === size && v.color.trim() === color && v.stock > 0);
  }

  isColorAvailable(color: string): boolean {
    const p = this.product();
    if (!p) return false;
    const size = this.selectedSize();
    if (!size) return p.variants.some(v => v.color.trim() === color && v.stock > 0);
    return p.variants.some(v => v.color.trim() === color && v.size.trim() === size && v.stock > 0);
  }

  selectSize(size: string): void {
    if (!this.isSizeAvailable(size)) return;
    this.selectedSize.set(this.selectedSize() === size ? null : size);
    this.sizeError.set(false);
  }

  selectColor(color: string): void {
    if (!this.isColorAvailable(color)) return;
    this.selectedColor.set(this.selectedColor() === color ? null : color);
    this.colorError.set(false);
  }

  decrement(): void {
    if (this.quantity() > 1) this.quantity.update(q => q - 1);
  }

  increment(): void {
    this.quantity.update(q => q + 1);
  }

  addToCart(): void {
    const p = this.product();
    if (!p) return;

    if (!this.selectedSize()) {
      this.sizeError.set(true);
    }
    if (this.colors().length > 0 && !this.selectedColor()) {
      this.colorError.set(true);
    }
    if (!this.selectedSize() || (this.colors().length > 0 && !this.selectedColor())) {
      return;
    }

    const size = this.selectedSize()!;
    const color = this.selectedColor() ?? '';

    const variant = p.variants.find(v => v.size.trim() === size && v.color.trim() === color)
      ?? p.variants.find(v => v.size.trim() === size)
      ?? p.variants[0];

    if (!variant) return;

    this.cartService.addItem({
      variantId: variant.id,
      productId: p.id,
      name: p.name,
      slug: p.slug,
      imageUrl: this.images()[0],
      color: variant.color,
      size: variant.size,
      price: Number(p.price),
      quantity: this.quantity(),
    });

    this.addedToCart.set(true);
    setTimeout(() => this.addedToCart.set(false), 2000);
  }

  addToWishlist(): void {
    const p = this.product();
    if (!p) return;
    this.wishlistService.toggle({
      productId: p.id,
      name: p.name,
      slug: p.slug,
      imageUrl: this.images()[0],
      price: Number(p.price),
      category: p.category.name,
    });
    this.addedToWishlist.set(true);
    setTimeout(() => this.addedToWishlist.set(false), 2000);
  }
}
