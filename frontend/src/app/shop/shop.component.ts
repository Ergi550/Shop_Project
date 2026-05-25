import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';
import { LayoutComponent } from '../layout/layout.component';
import { ProductService } from '../core/services/product.service';
import { Product } from '../core/models';
import { productImage } from '../core/product-images';

const CATEGORY_TITLES: Record<string, string> = {
  all: 'All Products',
  dresses: 'Dresses',
  tops: 'Tops',
  shoes: 'Shoes',
  accessories: 'Accessories',
  'new-arrivals': 'New Arrivals',
  sale: 'Sale',
};

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

  private slugParam = toSignal(
    this.route.paramMap.pipe(map(p => p.get('slug') ?? 'all')),
    { initialValue: 'all' }
  );

  sortBy = signal('featured');

  private allProductsRaw = toSignal(this.productService.getProducts());
  readonly loading = computed(() => this.allProductsRaw() === undefined);
  readonly error = signal('');

  private allProducts = computed<Product[]>(() => this.allProductsRaw() ?? []);

  readonly filterTabs = [
    { label: 'All',         slug: 'all' },
    { label: 'Dresses',     slug: 'dresses' },
    { label: 'Tops',        slug: 'tops' },
    { label: 'Shoes',       slug: 'shoes' },
    { label: 'Accessories', slug: 'accessories' },
  ];

  categoryTitle = computed(() => CATEGORY_TITLES[this.slugParam()] ?? 'Shop');

  breadcrumb = computed(() => {
    const slug = this.slugParam();
    return slug && slug !== 'all' ? (CATEGORY_TITLES[slug] ?? slug) : null;
  });

  activeTab = computed(() => {
    const slug = this.slugParam();
    return this.filterTabs.some(t => t.slug === slug) ? slug : 'all';
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
}
