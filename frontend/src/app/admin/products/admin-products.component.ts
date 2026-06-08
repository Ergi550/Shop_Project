import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { forkJoin, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { AdminService } from '../admin.service';
import { AdminCategory, AdminProductSummary, AdminProductDetail, AdminVariant } from '../admin-models';

interface ColorEntry {
  id?: number;
  color: string;
  stock: number;
}

interface SizeGroup {
  size: string;
  colors: ColorEntry[];
}

@Component({
  selector: 'app-admin-products',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-products.component.html',
})
export class AdminProductsComponent implements OnInit {
  private svc = inject(AdminService);

  // List state
  products = signal<AdminProductSummary[]>([]);
  categories = signal<AdminCategory[]>([]);
  loading = signal(true);
  error = signal('');
  search = signal('');
  deleteConfirmId = signal<number | null>(null);

  // Form state
  view = signal<'list' | 'form'>('list');
  editingId = signal<number | null>(null);
  saving = signal(false);
  formError = signal('');
  form = signal({
    name: '', slug: '', description: '',
    price: '', category: '', available: true,
  });
  sizeGroups = signal<SizeGroup[]>([]);
  deletedVariantIds = signal<number[]>([]);
  imageFile = signal<File | null>(null);
  imagePreview = signal<string | null>(null);
  existingImage = signal<string | null>(null);

  ngOnInit(): void {
    this.loadCategories();
    this.loadProducts();
  }

  loadCategories(): void {
    this.svc.getCategories().subscribe({ next: cats => this.categories.set(cats) });
  }

  loadProducts(): void {
    this.loading.set(true);
    this.svc.getProducts(this.search()).subscribe({
      next: p => { this.products.set(p); this.loading.set(false); },
      error: () => { this.error.set('Failed to load products.'); this.loading.set(false); },
    });
  }

  onSearch(val: string): void {
    this.search.set(val);
    this.loadProducts();
  }

  // ── Form ──────────────────────────────────────────────────────────

  openCreate(): void {
    this.editingId.set(null);
    this.form.set({ name: '', slug: '', description: '', price: '', category: '', available: true });
    this.sizeGroups.set([]);
    this.deletedVariantIds.set([]);
    this.imageFile.set(null);
    this.imagePreview.set(null);
    this.existingImage.set(null);
    this.formError.set('');
    this.view.set('form');
  }

  openEdit(id: number): void {
    this.formError.set('');
    this.svc.getProduct(id).subscribe({
      next: p => {
        this.editingId.set(p.id);
        this.form.set({
          name: p.name, slug: p.slug, description: p.description,
          price: String(p.price), category: String(p.category), available: p.available,
        });
        // Group flat variants by size
        const grouped = new Map<string, ColorEntry[]>();
        for (const v of p.variants) {
          if (!grouped.has(v.size)) grouped.set(v.size, []);
          grouped.get(v.size)!.push({ id: v.id, color: v.color, stock: v.stock });
        }
        this.sizeGroups.set([...grouped.entries()].map(([size, colors]) => ({ size, colors })));
        this.deletedVariantIds.set([]);
        this.imageFile.set(null);
        this.imagePreview.set(null);
        this.existingImage.set(p.image);
        this.view.set('form');
      },
      error: () => this.error.set('Failed to load product.'),
    });
  }

  backToList(): void { this.view.set('list'); this.loadProducts(); }

  updateField(field: string, value: string | boolean): void {
    this.form.update(f => ({ ...f, [field]: value }));
  }

  onImageChange(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    this.imageFile.set(file);
    const reader = new FileReader();
    reader.onload = e => this.imagePreview.set(e.target?.result as string);
    reader.readAsDataURL(file);
  }

  // ── Size Groups ───────────────────────────────────────────────────

  addSizeGroup(): void {
    this.sizeGroups.update(gs => [...gs, { size: '', colors: [{ color: '', stock: 0 }] }]);
  }

  removeSizeGroup(si: number): void {
    const group = this.sizeGroups()[si];
    const ids = group.colors.filter(c => c.id).map(c => c.id!);
    if (ids.length) this.deletedVariantIds.update(prev => [...prev, ...ids]);
    this.sizeGroups.update(gs => gs.filter((_, i) => i !== si));
  }

  updateSize(si: number, value: string): void {
    this.sizeGroups.update(gs => gs.map((g, i) => i === si ? { ...g, size: value } : g));
  }

  // ── Colors within a size ─────────────────────────────────────────

  addColorToSize(si: number): void {
    this.sizeGroups.update(gs => gs.map((g, i) =>
      i === si ? { ...g, colors: [...g.colors, { color: '', stock: 0 }] } : g
    ));
  }

  removeColor(si: number, ci: number): void {
    const entry = this.sizeGroups()[si].colors[ci];
    if (entry.id) this.deletedVariantIds.update(ids => [...ids, entry.id!]);
    this.sizeGroups.update(gs => gs.map((g, i) =>
      i === si ? { ...g, colors: g.colors.filter((_, j) => j !== ci) } : g
    ));
  }

  updateColor(si: number, ci: number, field: keyof ColorEntry, value: string | number): void {
    this.sizeGroups.update(gs => gs.map((g, i) =>
      i === si
        ? { ...g, colors: g.colors.map((c, j) => j === ci ? { ...c, [field]: value } : c) }
        : g
    ));
  }

  // ── Save ──────────────────────────────────────────────────────────

  save(): void {
    const f = this.form();
    if (!f.name.trim()) { this.formError.set('Product name is required.'); return; }
    if (!f.price || isNaN(Number(f.price))) { this.formError.set('A valid price is required.'); return; }
    if (!f.category) { this.formError.set('Please select a category.'); return; }

    this.saving.set(true);
    this.formError.set('');

    const fd = new FormData();
    fd.append('name', f.name.trim());
    fd.append('description', f.description);
    fd.append('price', f.price);
    fd.append('category', f.category);
    fd.append('available', String(f.available));
    if (f.slug.trim()) fd.append('slug', f.slug.trim());
    if (this.imageFile()) fd.append('image', this.imageFile()!);

    // Flatten size groups → flat variant list
    const allVariants = this.sizeGroups().flatMap(g =>
      g.colors.map(c => ({ id: c.id, size: g.size, color: c.color, stock: c.stock }))
    );

    const productObs = this.editingId()
      ? this.svc.updateProduct(this.editingId()!, fd)
      : this.svc.createProduct(fd);

    productObs.pipe(
      switchMap(product => {
        const ops: any[] = [];
        for (const id of this.deletedVariantIds()) {
          ops.push(this.svc.deleteVariant(id));
        }
        for (const v of allVariants.filter(v => !v.id)) {
          ops.push(this.svc.createVariant(product.id, { size: v.size, color: v.color, stock: v.stock }));
        }
        for (const v of allVariants.filter(v => !!v.id)) {
          ops.push(this.svc.updateVariant(v.id!, { size: v.size, color: v.color, stock: v.stock }));
        }
        return ops.length ? forkJoin(ops) : of(null);
      })
    ).subscribe({
      next: () => { this.saving.set(false); this.backToList(); },
      error: (err) => { this.saving.set(false); this.formError.set(err?.error?.detail ?? 'Save failed. Check all fields.'); },
    });
  }

  // ── Delete ────────────────────────────────────────────────────────

  confirmDelete(id: number): void { this.deleteConfirmId.set(id); }
  cancelDelete(): void { this.deleteConfirmId.set(null); }

  doDelete(id: number): void {
    this.svc.deleteProduct(id).subscribe({
      next: () => { this.deleteConfirmId.set(null); this.loadProducts(); },
      error: () => { this.error.set('Delete failed.'); this.deleteConfirmId.set(null); },
    });
  }
}
