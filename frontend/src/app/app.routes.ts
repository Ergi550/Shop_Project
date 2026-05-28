import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ShopComponent } from './shop/shop.component';
import { ProductDetailComponent } from './product-detail/product-detail.component';
import { CartComponent } from './cart/cart.component';
import { WishlistComponent } from './wishlist/wishlist.component';
import { CheckoutComponent } from './checkout/checkout.component';
import { OrderConfirmationComponent } from './order-confirmation/order-confirmation.component';
import { LoginComponent } from './auth/login.component';
import { RegisterComponent } from './auth/register.component';
import { MyOrdersComponent } from './orders/my-orders.component';
import { AdminComponent } from './admin/admin.component';
import { AdminDashboardComponent } from './admin/dashboard/admin-dashboard.component';
import { AdminProductsComponent } from './admin/products/admin-products.component';
import { AdminCategoriesComponent } from './admin/categories/admin-categories.component';
import { AdminOrdersComponent } from './admin/orders/admin-orders.component';
import { authGuard } from './core/guards/auth.guard';
import { adminGuard } from './core/guards/admin.guard';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'shop', component: ShopComponent },
  { path: 'category/:slug', component: ShopComponent },
  { path: 'product/:slug', component: ProductDetailComponent },
  { path: 'cart', component: CartComponent },
  { path: 'wishlist', component: WishlistComponent },
  { path: 'checkout', component: CheckoutComponent, canActivate: [authGuard] },
  { path: 'order-confirmation', component: OrderConfirmationComponent, canActivate: [authGuard] },
  { path: 'orders', component: MyOrdersComponent, canActivate: [authGuard] },
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [adminGuard],
    children: [
      { path: '',           redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard',  component: AdminDashboardComponent  },
      { path: 'products',   component: AdminProductsComponent   },
      { path: 'categories', component: AdminCategoriesComponent },
      { path: 'orders',     component: AdminOrdersComponent     },
    ],
  },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: '**', redirectTo: '' },
];
