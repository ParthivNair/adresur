-- Add batch orders table to group multiple orders together
-- This addresses the issue where multiple items in a cart create separate orders

-- Batch orders table to group related orders
CREATE TABLE IF NOT EXISTS batch_orders (
    id SERIAL PRIMARY KEY,
    buyer_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    total_price DECIMAL(10,2) NOT NULL CHECK (total_price > 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' 
        CHECK (status IN ('pending', 'preparing', 'ready', 'completed', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add batch_order_id to orders table to link orders to batches
ALTER TABLE orders ADD COLUMN IF NOT EXISTS batch_order_id INTEGER REFERENCES batch_orders(id) ON DELETE CASCADE;

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_batch_orders_buyer_id ON batch_orders(buyer_id);
CREATE INDEX IF NOT EXISTS idx_batch_orders_status ON batch_orders(status);
CREATE INDEX IF NOT EXISTS idx_batch_orders_created_at ON batch_orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_batch_order_id ON orders(batch_order_id);

-- Add trigger for batch_orders updated_at
CREATE TRIGGER update_batch_orders_updated_at BEFORE UPDATE ON batch_orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); 