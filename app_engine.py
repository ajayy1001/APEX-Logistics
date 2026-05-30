from structures import InventoryLinkedList, OrderQueue

class DashboardManagementEngine:
    def __init__(self):
        self.inventory = InventoryLinkedList()
        self.order_pipeline = OrderQueue()

    def get_inventory_list(self):
        items = []
        current = self.inventory.head
        while current:
            status = "⚠️ LOW STOCK" if current.quantity <= current.threshold else "✅ OK"
            items.append({
                "ID": current.item_id,
                "Item Name": current.name,
                "Category": current.category,
                "Quantity": current.quantity,
                "Price ($)": f"${current.price:.2f}",
                "RawPrice": current.price,
                "Threshold": current.threshold,
                "Status": status
            })
            current = current.next
        return items

    def get_system_metrics(self):
        """Computes live infrastructure analytics counters for dashboard presentation."""
        total_items = 0
        total_value = 0.0
        low_stock_count = 0
        
        current = self.inventory.head
        while current:
            total_items += current.quantity
            total_value += (current.quantity * current.price)
            if current.quantity <= current.threshold:
                low_stock_count += 1
            current = current.next
            
        return {
            "Total Units": total_items,
            "Inventory Value": f"${total_value:,.2f}",
            "Alert Items": low_stock_count
        }

    def get_queue_list(self):
        orders = []
        current = self.order_pipeline.front
        while current:
            orders.append({
                "Order ID": current.order_id,
                "Target Item ID": current.item_id,
                "Quantity Requested": current.quantity_requested
            })
            current = current.next
        return orders

    def run_binary_search(self, search_id):
        node = self.inventory.binary_search_inventory(search_id)
        if node:
            return {
                "Found": True,
                "Data": {
                    "ID": node.item_id,
                    "Name": node.name,
                    "Category": node.category,
                    "Quantity": node.quantity,
                    "Price": f"${node.price:.2f}",
                    "Status": "⚠️ LOW STOCK" if node.quantity <= node.threshold else "✅ OK"
                }
            }
        return {"Found": False}

    def process_next_order(self):
        order = self.order_pipeline.dequeue_order()
        if not order:
            return {"type": "info", "msg": "Order execution pipeline is completely empty."}

        item = self.inventory.binary_search_inventory(order.item_id)
        if not item:
            return {"type": "error", "msg": f"Order {order.order_id} FAILED: Item ID {order.item_id} does not exist."}

        if item.quantity >= order.quantity_requested:
            item.quantity -= order.quantity_requested
            msg = f"Order {order.order_id} Dispatched! {order.quantity_requested} units of '{item.name}' moved out."
            if item.quantity <= item.threshold:
                return {
                    "type": "success_alert", 
                    "msg": msg, 
                    "alert": f"🚨 AUTOMATED PROCUREMENT TRIGGERED: '{item.name}' requires immediate restocking!"
                }
            return {"type": "success", "msg": msg}
        else:
            return {
                "type": "warning", 
                "msg": f"Order {order.order_id} BACKORDERED: Insufficient stock for '{item.name}'."
            }