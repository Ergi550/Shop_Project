import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Product } from '../models';

@Injectable({ providedIn: 'root' })
export class ProductService {
  private http = inject(HttpClient);
  private api = environment.apiUrl;

  getProducts(categorySlug?: string): Observable<Product[]> {
    let params = new HttpParams();
    if (categorySlug) params = params.set('category', categorySlug);
    return this.http.get<Product[]>(`${this.api}/products/`, { params });
  }

  getProduct(slug: string): Observable<Product> {
    return this.http.get<Product>(`${this.api}/products/${slug}/`);
  }
}
