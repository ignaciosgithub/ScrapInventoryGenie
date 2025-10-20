import os
import sys
from database import InventoryDatabase

def test_database():
    print("Testing Scrap Inventory Genie Database...")
    print("-" * 50)
    
    test_db_path = "test_inventory.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    db = InventoryDatabase(test_db_path)
    
    print("\n1. Testing Box Operations...")
    box_id = db.add_box("Test Box 1", "Shelf A", "A test storage box")
    print(f"   Created box with ID: {box_id}")
    
    boxes = db.get_boxes()
    print(f"   Total boxes: {len(boxes)}")
    assert len(boxes) == 1, "Should have 1 box"
    
    print("\n2. Testing Material Operations...")
    material_id = db.add_material(
        name="Red Paper",
        box_id=box_id,
        brand="BrandA",
        material_type="Paper",
        width=20.0,
        height=30.0,
        depth=0.5,
        unit="cm",
        quantity=5,
        color="Red",
        tutorial_url="http://example.com",
        notes="Test material"
    )
    print(f"   Created material with ID: {material_id}")
    
    materials = db.get_materials()
    print(f"   Total materials: {len(materials)}")
    assert len(materials) == 1, "Should have 1 material"
    
    print("\n3. Testing Material Search...")
    results = db.search_materials(name="Red", brand="BrandA")
    print(f"   Search results: {len(results)}")
    assert len(results) == 1, "Should find 1 material"
    
    print("\n4. Testing Mark as Used...")
    db.mark_material_used(material_id, True)
    material = db.get_material(material_id)
    print(f"   Material is_used: {material['is_used']}")
    assert material['is_used'] == 1, "Material should be marked as used"
    
    print("\n5. Testing Project Operations...")
    project_id = db.add_project("Test Project", "A test project")
    print(f"   Created project with ID: {project_id}")
    
    projects = db.get_projects()
    print(f"   Total projects: {len(projects)}")
    assert len(projects) == 1, "Should have 1 project"
    
    print("\n6. Testing Project Materials...")
    pm_id = db.add_project_material(project_id, material_id, 2)
    print(f"   Added material to project with ID: {pm_id}")
    
    project_materials = db.get_project_materials(project_id)
    print(f"   Materials in project: {len(project_materials)}")
    assert len(project_materials) == 1, "Should have 1 material in project"
    
    print("\n7. Testing Update Operations...")
    db.update_material(material_id, quantity=10, color="Dark Red")
    material = db.get_material(material_id)
    print(f"   Updated material quantity: {material['quantity']}")
    print(f"   Updated material color: {material['color']}")
    assert material['quantity'] == 10, "Quantity should be updated"
    assert material['color'] == "Dark Red", "Color should be updated"
    
    print("\n8. Testing Bulk Operations...")
    for i in range(5):
        db.add_material(
            name=f"Material {i+2}",
            brand=f"Brand{i}",
            material_type="Test",
            width=10.0 + i,
            height=15.0 + i,
            quantity=i+1
        )
    
    all_materials = db.get_materials()
    print(f"   Total materials after bulk add: {len(all_materials)}")
    assert len(all_materials) == 6, "Should have 6 materials"
    
    print("\n9. Testing Dimension Filters...")
    results = db.search_materials(min_width=12.0, max_width=14.0)
    print(f"   Materials with width 12-14: {len(results)}")
    
    db.close()
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    print("\n" + "=" * 50)
    print("All tests passed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        test_database()
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
