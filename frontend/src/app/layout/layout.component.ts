import { Component, HostListener, Input, OnInit, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { CartService } from '../core/services/cart.service';
import { AuthService } from '../core/services/auth.service';
import { CategoryService } from '../core/services/category.service';
import { ProductService } from '../core/services/product.service';
import { SizeGuideService } from '../core/services/size-guide.service';
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
  sizeGuide = inject(SizeGuideService);
  private categoryService = inject(CategoryService);
  private productService = inject(ProductService);
  private router = inject(Router);

  scrolled = signal(false);
  menuOpen = signal(false);
  searchOpen = signal(false);
  accountOpen = signal(false);
  searchQuery = signal('');
  sizeGuideTab = signal<'clothing' | 'shoes'>('clothing');
  contactOpen = signal(false);

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

  readonly clothingSizes = [
    { label: 'XXS', eu: '32', uk: '4',      us: '00',    bust: '74–76', waist: '58–60', hips: '80–82' },
    { label: 'XS',  eu: '34', uk: '6',      us: '0–2',   bust: '78–80', waist: '62–64', hips: '86–88' },
    { label: 'S',   eu: '36', uk: '8–10',   us: '4–6',   bust: '82–85', waist: '65–68', hips: '90–94' },
    { label: 'M',   eu: '38', uk: '12',     us: '8',     bust: '87–89', waist: '70–73', hips: '96–99' },
    { label: 'L',   eu: '40', uk: '14–16',  us: '10–12', bust: '91–94', waist: '75–78', hips: '101–104' },
    { label: 'XL',  eu: '42', uk: '18–20',  us: '14–16', bust: '96–99', waist: '81–84', hips: '106–109' },
    { label: 'XXL', eu: '44', uk: '22–24',  us: '18–20', bust: '101–104', waist: '87–90', hips: '111–114' },
    { label: '3XL', eu: '46', uk: '26–28',  us: '22–24', bust: '106–109', waist: '93–96', hips: '116–119' },
    { label: '4XL', eu: '48', uk: '30–32',  us: '26–28', bust: '111–114', waist: '99–102', hips: '121–124' },
  ];

  readonly shoeSizes = [
    { eu: '34', uk: '1.5–2',   us: '3–3.5',   length: '21.5' },
    { eu: '35', uk: '2–2.5',   us: '4–4.5',   length: '22.0' },
    { eu: '36', uk: '3–3.5',   us: '5–5.5',   length: '22.5' },
    { eu: '37', uk: '4–4.5',   us: '6–6.5',   length: '23.5' },
    { eu: '38', uk: '5–5.5',   us: '7–7.5',   length: '24.0' },
    { eu: '39', uk: '6–6.5',   us: '8–8.5',   length: '25.0' },
    { eu: '40', uk: '7–7.5',   us: '9–9.5',   length: '25.5' },
    { eu: '41', uk: '8–8.5',   us: '10–10.5', length: '26.5' },
    { eu: '42', uk: '9–9.5',   us: '11–11.5', length: '27.0' },
    { eu: '43', uk: '10–10.5', us: '12–12.5', length: '28.0' },
    { eu: '44', uk: '11–11.5', us: '13–13.5', length: '28.5' },
    { eu: '45', uk: '12–12.5', us: '14–14.5', length: '29.5' },
  ];
}
