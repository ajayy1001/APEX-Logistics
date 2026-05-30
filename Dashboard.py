import streamlit as st
import pandas as pd
from app_engine import DashboardManagementEngine

if "engine" not in st.session_state:
    st.session_state.engine = DashboardManagementEngine()
    engine = st.session_state.engine
    
    # SEEDING 15 GENUINE INFRASTRUCTURE PRODUCTION ITEMS BY CATEGORY
    # Category 1: Networking Hardware
    engine.inventory.insert_item(101, "Network Switch 24P", "Networking Hardware", 14, 350.00, 4)
    engine.inventory.insert_item(102, "Core Enterprise Router", "Networking Hardware", 6, 1250.00, 2)
    engine.inventory.insert_item(103, "Hardware Firewall Appliance", "Networking Hardware", 3, 890.00, 2)
    engine.inventory.insert_item(104, "Wireless Access Point Wifi6", "Networking Hardware", 25, 120.00, 5)
    
    # Category 2: Fiber Optics
    engine.inventory.insert_item(201, "Fiber Optic Cable SM 10m", "Fiber Optics", 80, 15.50, 15)
    engine.inventory.insert_item(202, "SFP+ Transceiver Module", "Fiber Optics", 45, 85.00, 10)
    engine.inventory.insert_item(203, "High-Density Patch Panel", "Fiber Optics", 12, 110.00, 3)
    engine.inventory.insert_item(204, "Optical Fusion Splicer", "Fiber Optics", 2, 2400.00, 1)
    
    # Category 3: Server Infrastructure
    engine.inventory.insert_item(301, "Rack Server 2U Intel Xeon", "Server Infrastructure", 8, 4500.00, 2)
    engine.inventory.insert_item(302, "32GB DDR5 ECC Server RAM", "Server Infrastructure", 60, 180.00, 12)
    engine.inventory.insert_item(303, "2TB NVMe PCIe4 Enterprise SSD", "Server Infrastructure", 40, 290.00, 8)
    engine.inventory.insert_item(304, "Hot-Swap Redundant Power Supply", "Server Infrastructure", 15, 210.00, 4)
    engine.inventory.insert_item(305, "Liquid Cooling Manifold Unit", "Server Infrastructure", 5, 620.00, 2)
    
    # Category 4: Power & Enclosures
    engine.inventory.insert_item(401, "42U Server Rack Enclosure", "Power & Enclosures", 7, 950.00, 2)
    engine.inventory.insert_item(402, "Smart PDU 16-Outlet Metered", "Power & Enclosures", 11, 310.00, 3)

engine = st.session_state.engine
VALID_CATEGORIES = ["Networking Hardware", "Fiber Optics", "Server Infrastructure", "Power & Enclosures"]

# --- LAYOUT THEMING ---
st.set_page_config(page_title="Apex Logistics Corp.", layout="wide", page_icon="🏢")
st.title("🏢 Apex Logistics Corp.")
st.subheader("High-Throughput Inventory Optimization Using Dynamic Linked Lists & FIFO Queues")
st.markdown("---")

# =====================================================================
# SIDEBAR CONTROL CENTER
# =====================================================================
st.sidebar.header("🕹️ Dispatch System Controls")

if st.sidebar.button("⚙️ Fulfill Next Order (Dequeue)", use_container_width=True):
    log = engine.process_next_order()
    if log["type"] == "info": st.sidebar.info(log["msg"])
    elif log["type"] == "error": st.sidebar.error(log["msg"])
    elif log["type"] == "warning": st.sidebar.warning(log["msg"])
    elif log["type"] == "success": st.sidebar.success(log["msg"])
    elif log["type"] == "success_alert":
        st.sidebar.success(log["msg"])
        st.sidebar.warning(log["alert"])

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Real-Time Operations Metrics")
metrics = engine.get_system_metrics()
st.sidebar.metric(label="Total Stock Units On-Hand", value=metrics["Total Units"])
st.sidebar.metric(label="Gross Valuation Asset Pool", value=metrics["Inventory Value"])
if metrics["Alert Items"] > 0:
    st.sidebar.error(f"🚨 Low Stock Alerts Active: {metrics['Alert Items']} items")
else:
    st.sidebar.success("✅ All Stock Buffers Normal")

st.sidebar.markdown("---")
st.sidebar.subheader("⚡ Algorithmic Operations")
sort_option = st.sidebar.selectbox("Sort Metric Criteria", ["ID", "Quantity", "Category"])
if st.sidebar.button("⚡ Sort Inventory (Merge Sort)", use_container_width=True):
    engine.inventory.merge_sort_inventory(sort_by=sort_option)
    st.sidebar.success(f"Linked List re-ordered by {sort_option} using Merge Sort!")

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ System Configuration Adjuster"):
    st.caption("Override global tracking limits safely")
    override_id = st.number_input("Target Item ID", min_value=1, step=1, value=101)
    new_thresh = st.number_input("New Alert Limit", min_value=1, step=1, value=5)
    if st.button("Apply Safety Buffer Update"):
        target_node = engine.inventory.binary_search_inventory(override_id)
        if target_node:
            target_node.threshold = new_thresh
            st.sidebar.success(f"Threshold for ID {override_id} set to {new_thresh} units.")
            st.rerun()
        else:
            st.sidebar.error("Item ID not found.")

# =====================================================================
# MAIN WINDOW LAYOUT
# =====================================================================
col1, col2 = st.columns([3, 2])

with col1:
    st.header("🗄️ Core Warehouse Inventory Records")
    selected_cat_filter = st.selectbox("📂 Filter Dashboard Catalog View by Category", ["Show All Components"] + VALID_CATEGORIES)
    
    inventory_data = engine.get_inventory_list()
    if inventory_data:
        df_inv = pd.DataFrame(inventory_data)
        if selected_cat_filter != "Show All Components":
            df_inv = df_inv[df_inv["Category"] == selected_cat_filter]
        st.dataframe(df_inv.drop(columns=["RawPrice"]), use_container_width=True, hide_index=True)
    else:
        st.info("Inventory linked list is currently empty.")

    st.markdown("### 🔍 High-Speed Product Query Tool")
    with st.form("search_form"):
        search_id = st.number_input("Target Product ID to Query via Binary Search", min_value=1, step=1, value=101)
        if st.form_submit_button("Execute Binary Search"):
            result = engine.run_binary_search(search_id)
            if result["Found"]:
                st.success(f"**Item Located!** Name: `{result['Data']['Name']}` | Category: `{result['Data']['Category']}` | Stock Level: `{result['Data']['Quantity']}` | Health Status: `{result['Data']['Status']}`")
            else:
                st.error(f"Product ID {search_id} not found in sorted search parameters.")

    with st.expander("➕ Link New Inventory Item Node (With Category Assignments)"):
        with st.form("add_item_form", clear_on_submit=True):
            item_id = st.number_input("Item ID", min_value=1, step=1, value=105)
            name = st.text_input("Item Name", value="Cat6 Patch Panel")
            category = st.selectbox("Assign Storage Logistics Category", VALID_CATEGORIES)
            qty = st.number_input("Initial Quantity Stock", min_value=0, step=1, value=15)
            price = st.number_input("Unit Cost ($)", min_value=0.0, step=0.01, value=45.00)
            thresh = st.number_input("Low Stock Warning Safety Buffer", min_value=1, step=1, value=5)
            
            if st.form_submit_button("Append Node to Inventory"):
                if engine.inventory.insert_item(item_id, name, category, qty, price, thresh):
                    st.success(f"Successfully linked '{name}' into data registers.")
                    st.rerun()
                else:
                    st.error("Operation Denied: Item ID already exists.")

    with st.expander("❌ Drop/Discontinue Stock Profile Node"):
        with st.form("delete_item_form", clear_on_submit=True):
            del_id = st.number_input("Target Item ID to Expunge", min_value=1, step=1)
            if st.form_submit_button("Sever Pointer Connections"):
                if engine.inventory.delete_item(del_id):
                    st.success(f"Item Node {del_id} dropped from memory pointers.")
                    st.rerun()
                else:
                    st.error("Exception Error: Item ID mismatch. Deletion sequence aborted.")

with col2:
    st.header("⏳ Outbound Order Pipeline (FIFO)")
    queue_data = engine.get_queue_list()
    if queue_data:
        st.dataframe(pd.DataFrame(queue_data), use_container_width=True, hide_index=True)
    else:
        st.success("🎉 Order pipeline clear. All requests dispatched!")

    st.markdown("### 📥 Accept New Order Entry")
    with st.form("order_form", clear_on_submit=True):
        order_id = st.text_input("Create Order Track ID", value="ORD-9901")
        target_id = st.number_input("Target Item ID Requested", min_value=1, step=1, value=101)
        req_qty = st.number_input("Allocation Quantity", min_value=1, step=1, value=5)
        
        if st.form_submit_button("Queue Order Request"):
            item = engine.inventory.find_item(target_id)
            if not item:
                st.error(f"Order Rejected: Item ID {target_id} does not exist in inventory records.")
            else:
                engine.order_pipeline.enqueue_order(order_id, target_id, req_qty)
                st.success(f"Order {order_id} placed in FIFO pipeline.")
                st.rerun()