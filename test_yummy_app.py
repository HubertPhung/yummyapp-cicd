import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# ================================================================
# CAP DO 1: Bo test co ban cho san (Moi chi dat ~35% Coverage)
# ================================================================
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ================================================================
# CAP DO 2 (TIET 3): Test apply_promo_code
# ================================================================
class TestMediumLevel(unittest.TestCase):
    def test_promo_online_valid(self):
        app = YummyApp("online", 15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_promo_offline_raises(self):
        app = YummyApp("offline", 15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_special_code_os15(self):
        app = YummyApp("online", 15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_special_code_os14_raises(self):
        app = YummyApp("online", 14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


# ================================================================
# CAP DO 3 (TIET 3): Test get_nearby_restaurants bang Mocking
# ================================================================
class TestHardLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_in_zone(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        self.assertEqual(self.app.get_nearby_restaurants(),
                         ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"])

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_out_of_zone(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError()
        result = self.app.get_nearby_restaurants()
        self.assertIsInstance(result, str)
        self.assertIn("Khong the", result)


if __name__ == '__main__':
    unittest.main()