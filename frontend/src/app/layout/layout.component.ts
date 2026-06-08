import { Component, HostListener, Input, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { CartService } from '../core/services/cart.service';
import { AuthService } from '../core/services/auth.service';
import { CategoryService } from '../core/services/category.service';
import { ProductService } from '../core/services/product.service';
import { Product } from '../core/models';
import { productImage } from '../core/product-images';

interface NavCategory {
  name: string;
  slug: string;
}

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './layout.component.html',
})
export class LayoutComponent implements OnInit {
  @Input() solidNav = false;

  cart = inject(CartService);
  auth = inject(AuthService);
  private categoryService = inject(CategoryService);
  private productService = inject(ProductService);
  private router = inject(Router);

  scrolled = signal(false);
  menuOpen = signal(false);
  searchOpen = signal(false);
  accountOpen = signal(false);
  searchQuery = signal('');

  private dynamicCategories = signal<NavCategory[]>([]);
  private allProducts = signal<Product[]>([]);

  searchResults = computed(() => {
    const q = this.searchQuery().toLowerCase().trim();
    if (q.length < 2) return [];
    return this.allProducts()
      .filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.category.name.toLowerCase().includes(q)
      )
      .slice(0, 6);
  });

  get categories(): NavCategory[] {
    return [
      { name: 'New Arrivals', slug: 'new-arrivals' },
      ...this.dynamicCategories(),
      { name: 'Sale', slug: 'sale' },
    ];
  }

  ngOnInit(): void {
    this.categoryService.getCategories().subscribe(cats => {
      this.dynamicCategories.set(cats.map(c => ({ name: c.name, slug: c.slug })));
    });
    this.productService.getProducts().subscribe(products => {
      this.allProducts.set(products);
    });
  }

  @HostListener('window:scroll')
  onWindowScroll(): void {
    this.scrolled.set(window.scrollY > 50);
  }

  openMenu(): void {
    this.menuOpen.set(true);
    this.searchOpen.set(false);
    this.accountOpen.set(false);
  }

  closeMenu(): void {
    this.menuOpen.set(false);
  }

  openSearch(): void {
    this.searchOpen.set(true);
    this.menuOpen.set(false);
    this.accountOpen.set(false);
  }

  closeSearch(): void {
    this.searchOpen.set(false);
    this.searchQuery.set('');
  }

  onSearchInput(value: string): void {
    this.searchQuery.set(value);
  }

  selectSearchResult(slug: string): void {
    this.router.navigate(['/product', slug]);
    this.closeSearch();
  }

  productImageUrl(product: Product): string {
    return productImage(product.slug, product.image);
  }

  toggleAccount(): void {
    this.accountOpen.update(v => !v);
    this.menuOpen.set(false);
    this.searchOpen.set(false);
  }

  closeAccount(): void {
    this.accountOpen.set(false);
  }

  get navDark(): boolean {
    return this.solidNav || this.scrolled() || this.menuOpen() || this.searchOpen();
  }
}
