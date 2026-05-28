export interface AdminDashboard {
  total_products: number;
  available_products: number;
  total_orders: number;
  orders_by_status: Record<string, number>;
  recent_orders: AdminOrderSummary[];
  low_stock_variants: AdminLowStockVariant[];
}

export interface AdminOrderSummary {
  id: number;
  customer_email: string;
  customer_name: string;
  status: string;
  total: number;
  item_count: number;
  created_at: string;
}

export interface AdminLowStockVariant {
  id: number;
  product_id: number;
  product_name: string;
  size: string;
  color: string;
  stock: number;
}

export interface AdminCategory {
  id: number;
  name: string;
  slug: string;
  description: string;
  product_count: number;
}

export interface AdminVariant {
  id: number;
  size: string;
  color: string;
  stock: number;
}

export interface AdminProductSummary {
  id: number;
  name: string;
  slug: string;
  price: number;
  image: string | null;
  available: boolean;
  category: number;
  category_name: string;
  variant_count: number;
  total_stock: number;
  created_at: string;
}

export interface AdminProductDetail {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: number;
  image: string | null;
  available: boolean;
  category: number;
  category_name: string;
  variants: AdminVariant[];
  created_at: string;
  updated_At: string;
}

export interface AdminCustomer {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface AdminOrderItemVariant {
  id: number;
  product_id: number;
  product_name: string;
  size: string;
  color: string;
}

export interface AdminOrderItem {
  id: number;
  variant: AdminOrderItemVariant;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface AdminOrderDetail {
  id: number;
  customer: AdminCustomer;
  status: string;
  total: number;
  shipping_full_name: string;
  shipping_address: string;
  shipping_city: string;
  shipping_postcode: string;
  shipping_country: string;
  shipping_phone: string;
  items: AdminOrderItem[];
  created_at: string;
  updated_at: string;
}
