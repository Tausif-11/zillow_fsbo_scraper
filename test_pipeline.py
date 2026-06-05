import unittest
import pandas as pd
import pipeline

class TestZillowPipeline(unittest.TestCase):
    
    def test_parse_and_transform_routing(self):
        """Verifies parsing splits price reductions and marketing features cleanly."""
        # Mock payload mirroring Zillow's internal API response matrix
        mock_api_response = {
            "cat2": {
                "searchResults": {
                    "listResults": [
                        {
                            "zpid": "111111",
                            "price": "$500,000",
                            "detailUrl": "/homedetails/test/111111_zpid/",
                            "hdpData": {
                                "homeInfo": {
                                    "priceReduction": "$10,000 (May 20)",
                                    "homeType": "SINGLE_FAMILY",
                                    "city": "Houston",
                                    "state": "TX"
                                }
                            }
                        },
                        {
                            "zpid": "222222",
                            "price": "$650,000",
                            "flexFieldText": "Waterfront Lot",  # Marketing text fallback
                            "hdpData": {
                                "homeInfo": {
                                    "homeType": "CONDO",
                                    "city": "Dallas",
                                    "state": "TX"
                                }
                            }
                        }
                    ]
                }
            }
        }
        
        # Pass mock structural array through your pipeline
        df = pipeline.parse_and_transform(mock_api_response)
        
        # Test Assertions
        self.assertFalse(df.empty, "Pipeline returned an empty DataFrame.")
        self.assertEqual(len(df), 2, "Pipeline failed to extract exactly 2 records.")
        
        # Verify split-routing field fix logic is intact
        row_1 = df[df['ZPID'] == '111111'].iloc[0]
        row_2 = df[df['ZPID'] == '222222'].iloc[0]
        
        self.assertEqual(row_1['Price Reduction'], "$10,000 (May 20)")
        self.assertEqual(row_1['Marketing Features'], "None")
        
        self.assertEqual(row_2['Price Reduction'], "None")
        self.assertEqual(row_2['Marketing Features'], "Waterfront Lot")

if __name__ == '__main__':
    unittest.main()
