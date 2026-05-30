class ItemNode:
    """
    Represents a single node in the Inventory Linked List with structural categorizations.
    """
    def __init__(self, item_id, name, category, quantity, price, threshold=5):
        self.item_id = item_id
        self.name = name
        self.category = category  
        self.quantity = quantity
        self.price = price
        self.threshold = threshold
        self.next = None


class OrderNode:
    """
    Represents a single customer order node in the FIFO Queue.
    """
    def __init__(self, order_id, item_id, quantity_requested):
        self.order_id = order_id
        self.item_id = item_id
        self.quantity_requested = quantity_requested
        self.next = None