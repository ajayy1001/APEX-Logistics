from models import ItemNode, OrderNode

class InventoryLinkedList:
    """
    Handles linear dynamic storage operations for warehouse stock.
    """
    def __init__(self):
        self.head = None

    def insert_item(self, item_id, name, category, quantity, price, threshold=5):
        # Explicitly pass all 6 parameters into our verified model node
        new_node = ItemNode(item_id, name, category, quantity, price, threshold)
        if not self.head:
            self.head = new_node
            return True
        
        current = self.head
        while current:
            if current.item_id == item_id:
                return False  # Block duplicate IDs
            if current.next is None:
                break
            current = current.next
        
        current.next = new_node
        return True

    def delete_item(self, item_id):
        current = self.head
        prev = None

        while current:
            if current.item_id == item_id:
                if prev is None:  
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    def find_item(self, item_id):
        current = self.head
        while current:
            if current.item_id == item_id:
                return current
            current = current.next
        return None

    def merge_sort_inventory(self, sort_by="ID"):
        """ Core Merge Sort implementation mapping nodes to a list for sorting. """
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
            
        if not nodes:
            return

        def _merge_sort(arr):
            if len(arr) <= 1: return arr
            mid = len(arr) // 2
            left = _merge_sort(arr[:mid])
            right = _merge_sort(arr[mid:])
            return _merge(left, right)

        def _merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if sort_by == "ID":
                    v_l, v_r = left[i].item_id, right[j].item_id
                elif sort_by == "Category":
                    v_l, v_r = left[i].category, right[j].category
                else:
                    v_l, v_r = left[i].quantity, right[j].quantity

                if v_l <= v_r:
                    result.append(left[i]); i += 1
                else:
                    result.append(right[j]); j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        sorted_nodes = _merge_sort(nodes)
        
        self.head = sorted_nodes[0]
        for idx in range(len(sorted_nodes) - 1):
            sorted_nodes[idx].next = sorted_nodes[idx+1]
        sorted_nodes[-1].next = None

    def binary_search_inventory(self, target_id):
        """ Performs Binary Search on the index-mapped network array. """
        self.merge_sort_inventory(sort_by="ID")
        nodes = []
        current = self.head
        while current:
            nodes.append(current)
            current = current.next
            
        low, high = 0, len(nodes) - 1
        while low <= high:
            mid = (low + high) // 2
            if nodes[mid].item_id == target_id:
                return nodes[mid]
            elif nodes[mid].item_id < target_id:
                low = mid + 1
            else:
                high = mid - 1
        return None


class OrderQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue_order(self, order_id, item_id, quantity):
        new_order = OrderNode(order_id, item_id, quantity)
        if self.rear is None:
            self.front = self.rear = new_order
            return
        self.rear.next = new_order
        self.rear = new_order

    def dequeue_order(self):
        if self.front is None: return None
        temp = self.front
        self.front = self.front.next
        if self.front is None: self.rear = None
        return temp