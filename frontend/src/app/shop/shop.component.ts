import { Component, HostListener, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { LayoutComponent } from '../layout/layout.component';
import { ProductService } from '../core/services/product.service';
import { CategoryService } from '../core/services/category.service';
import { WishlistService } from '../core/services/wishlist.service';
import { Category, Product } from '../core/models';
import { productImage } from '../core/product-images';

const NEW_ARRIVAL_DAYS = 60;

@Component({
  selector: 'app-shop',
  standalone: true,
  imports: [CommonModule, RouterLink, LayoutComponent],
  templateUrl: './shop.component.html',
})
export class ShopComponent {
  private route = inject(ActivatedRoute);
  private productService = inject(ProductService);
  private categoryService = inject(CategoryService);
  wishlist = inject(WishlistService);

  private slugParam = toSignal(
    this.route.paramMap.pipe(map(p => p.get('slug') ?? 'all')),
    { initialValue: 'all' }
  );

  sortBy = signal('featured');
  sortOpen = signal(false);

  readonly sortOptions = [
    { value: 'featured',   label: 'Featured' },
    { value: 'newest',     label: 'New In' },
    { value: 'price-asc',  label: 'Price: Low — High' },
    { value: 'price-desc', label: 'Price: High — Low' },
  ];

  sortLabel = computed(() => this.sortOptions.find(o => o.value === this.sortBy())?.label ?? 'Featured');

  setSortBy(value: string): void {
    this.sortBy.set(value);
    this.sortOpen.set(false);
  }

  @HostListener('document:click')
  onDocumentClick(): void {
    this.sortOpen.set(false);
  }

  private allProductsRaw = toSignal(this.productService.getProducts());
  readonly loading = computed(() => this.allProductsRaw() === undefined);
  readonly error = signal('');

  private allProducts = computed<Product[]>(() => this.allProductsRaw() ?? []);

  private backendCategories = toSignal(this.categoryService.getCategories(), { initialValue: [] as Category[] });

  readonly filterTabs = computed(() => [
    { label: 'All', slug: 'all' },
    ...this.backendCategories().map(c => ({ label: c.name, slug: c.slug })),
  ]);

  categoryTitle = computed(() => {
    const slug = this.slugParam();
    if (slug === 'all') return 'All Products';
    if (slug === 'new-arrivals') return 'New Arrivals';
    if (slug === 'sale') return 'Sale';
    const cat = this.backendCategories().find(c => c.slug === slug);
    return cat ? cat.name : 'Shop';
  });

  breadcrumb = computed(() => {
    const slug = this.slugParam();
    if (!slug || slug === 'all') return null;
    if (slug === 'new-arrivals') return 'New Arrivals';
    if (slug === 'sale') return 'Sale';
    const cat = this.backendCategories().find(c => c.slug === slug);
    return cat ? cat.name : slug;
  });

  activeTab = computed(() => {
    const slug = this.slugParam();
    return this.filterTabs().some(t => t.slug === slug) ? slug : 'all';
  });

  filteredProducts = computed(() => {
    const slug = this.slugParam();
    const all = this.allProducts();
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - NEW_ARRIVAL_DAYS);

    let base: Product[];
    if (!slug || slug === 'all') {
      base = [...all];
    } else if (slug === 'new-arrivals') {
      base = all.filter(p => new Date(p.created_at) >= cutoff);
      if (!base.length) base = [...all].slice(0, 5);
    } else if (slug === 'sale') {
      base = all.filter(p => Number(p.price) < 300);
    } else {
      base = all.filter(p => p.category.slug === slug);
    }

    switch (this.sortBy()) {
      case 'price-asc':  return [...base].sort((a, b) => Number(a.price) - Number(b.price));
      case 'price-desc': return [...base].sort((a, b) => Number(b.price) - Number(a.price));
      case 'newest':     return [...base].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
      default:           return base;
    }
  });

  isNew(product: Product): boolean {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - NEW_ARRIVAL_DAYS);
    return new Date(product.created_at) >= cutoff;
  }

  imageUrl(product: Product): string {
    return productImage(product.slug, product.image);
  }

  toggleWishlist(event: Event, product: Product): void {
    event.preventDefault();
    event.stopPropagation();
    this.wishlist.toggle({
      productId: product.id,
      name: product.name,
      slug: product.slug,
      imageUrl: this.imageUrl(product),
      price: Number(product.price),
      category: product.category?.name,
      isNew: this.isNew(product),
    });
  }
}
