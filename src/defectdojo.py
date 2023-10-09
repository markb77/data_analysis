import logging
import os

import pandas as pd
import requests
from config import SUCCESS_STATUS_CODE
from dotenv import find_dotenv, load_dotenv


class DefectDojoAnalyzer:
    # Set Dependency Track instance base URL
    DEFECT_DOJO_BASE_URL = "https://vulnerabilitymgmt.poc.roche.com"  
    # Set API version
    API_VERSION = "v2"  
    # Set the API URL of your Dependency Track instance 
    DEFECT_DOJO_API_URL = f"{DEFECT_DOJO_BASE_URL}/api/{API_VERSION}"

    def __init__(self):
        # Set DefectDojo instance base URL
        self.producte_info = None

        # Load API_KEY
        load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=False))

        # Set API key
        self.API_KEY = os.getenv('DEFECT_DOJO_API_KEY')

        # Set header
        self.headers = {
            "Authorization": f"Token {self.API_KEY}",
            "content-type": "application/json",
        }

        self._get_products()
        if self.product_info is None:
            print("Initialization failed: Project information not available")  

    def _get_products(self, page_size=50):
        """
        Retrieves products from the DefectDojo API.

        Args:
            self: The DefectDojo instance.
            page_size: The number of products to retrieve per page.

        Returns:
            A DataFrame containing the product information if the request is successful, otherwise None.

        Example:
            ```python
            defect_dojo = DefectDojo()
            products = defect_dojo.get_products(page_size=50)
            if products is not None:
                print(products)
            else:
                print("Failed to get products.")
            ```
        """

        params = {'limit': str(page_size)}  # Set the limit parameter to retrieve the first 50 products
        url = f"{self.DEFECT_DOJO_API_URL}/products/?page_size={page_size}"
        response = self._make_request(method='GET', 
                                      url=url, 
                                      verify=False, 
                                      headers=self.headers, 
                                      params=params)

        if response and response.status_code == SUCCESS_STATUS_CODE:
            products = (response.json())['results']

            data = {
                'Name': [],
                'ID': []}
            for product in products:
                data['Name'].append(product['name']) 
                data['ID'].append(product['id']) 

            self.product_info = pd.DataFrame(data)
            return pd.DataFrame(data)

        logging.error(f"Failed to get projects. Status code: {response.status_code}" 
                      if response else "Failed to get projects.")
        return None
        
    # Function to get product information by ID
    def get_product_by_id(self, product_id):
        """
        Gets a product by its ID from the DefectDojo API.

        Args:
            self: The DefectDojo instance.
            product_id: The ID of the product to retrieve.

        Returns:
            A dictionary containing the name and ID of the product if the request is successful, otherwise None.

        Example:
            ```python
            defect_dojo = DefectDojo()
            product_id = 12345
            result = defect_dojo.get_product_by_id(product_id)
            if result is not None:
                print(result)
            else:
                print("Failed to get product.")
            ```
        """
        headers =  {                     
            "accept": "application/json",
            "Authorization": f"Token {self.API_KEY}"
        }      
        url = f"{self.DEFECT_DOJO_API_URL}/products/{product_id}/"
        response = self._make_request(method='GET', 
                                      url=url, 
                                      headers=headers, 
                                      verify=False)

        if response and response.status_code == SUCCESS_STATUS_CODE:
            product_data = response.json()
            return {'Name': product_data['name'], 'ID': product_data['id']}

        logging.error(f"Failed to get projects. Status code: {response.status_code}" 
                      if response else "Failed to get projects.")
        return None
      
    # Function to get engagements for a product by ID
    def get_engagements_for_product(self, product_id):
        """
        Gets engagements for a product by its ID from the DefectDojo API.

        Args:
            self: The DefectDojo instance.
            product_id: The ID of the product to retrieve engagements for.

        Returns:
            The response from the API call.

        Example:
            ```python
            defect_dojo = DefectDojo()
            product_id = 12345
            result = defect_dojo.get_engagements_for_product(product_id)
            print(result)
            ```
        """
        headers =  {                     
            "accept": "application/json",
            "Authorization": f"Token {self.API_KEY}"
        }      
        url = f"{self.DEFECT_DOJO_API_URL}/engagements/"
        params = {"product": product_id}

        response = self._make_request(method='GET', 
                                      url=url,
                                      params=params,
                                      headers=headers,
                                      verify=False)
        
       # Check the response status
        if response is not None and response.status_code == SUCCESS_STATUS_CODE:
            engagements = (response.json())['results']
            data = {
                "Name": [],
                "ID": []
            }
            for engagement in engagements:
                data["Name"].append(engagement["name"])
                # Check if the "version" key exists in the current project dictionary
                engagement.get("version", "None")  # Use "None" as the default value
                data["ID"].append(engagement["id"])       



            self.project_info = pd.DataFrame(data)
            return pd.DataFrame(data)
        else:
            logging.error("Failed to get projects.")
            return None
  
    def get_tests_for_engaggement(self, engagement_id):
 
        headers =  {                     
            "accept": "application/json",
            "Authorization": f"Token {self.API_KEY}"
        }      
        url = f"{self.DEFECT_DOJO_API_URL}/tests/"
        params = {"engagement": engagement_id}

        response = self._make_request(method='GET', 
                                      url=url,
                                      params=params,
                                      headers=headers,
                                      verify=False)
        
       # Check the response status
        if response is not None and response.status_code == SUCCESS_STATUS_CODE:
            tests = (response.json())['results']
            data = {
                "Test_Name": [],
                "Test_ID": [],
                "Test_Type_Name": [],
                "Scan_Type": [],
                "Test_Type_ID": [],
                "Engagement_ID": [],
                "Test_Title": [],

            }
            for test in tests:
                data["Name"].append(engagement["name"])

                # Check if the "version" key exists in the current project dictionary
                engagement.get("version", "None")  # Use "None" as the default value
                data["ID"].append(engagement["id"])       



            self.project_info = pd.DataFrame(data)
            return pd.DataFrame(data)
        else:
            logging.error("Failed to get projects.")
            return None

    def get_findings_for_test(self, test_id):
 
        headers =  {                     
            "accept": "application/json",
            "Authorization": f"Token {self.API_KEY}"
        }      
        url = f"{self.DEFECT_DOJO_API_URL}/findings/"
        params = {"test": test_id}

        response = self._make_request(method='GET', 
                                      url=url,
                                      params=params,
                                      headers=headers,
                                      verify=False)
        
       # Check the response status
        if response is not None and response.status_code == SUCCESS_STATUS_CODE:
            tests = (response.json())['results']
            data = {
                "Test_Name": [],
                "Test_ID": [],
                "Test_Type_Name": [],
                "Scan_Type": [],
                "Test_Type_ID": [],
                "Engagement_ID": [],
                "Test_Title": [],

            }
            for test in tests:
                data["Name"].append(engagement["name"])

                # Check if the "version" key exists in the current project dictionary
                engagement.get("version", "None")  # Use "None" as the default value
                data["ID"].append(engagement["id"])       



            self.project_info = pd.DataFrame(data)
            return pd.DataFrame(data)
        else:
            logging.error("Failed to get projects.")
            return None





    def get_engagements(self):
        url = f"{self.base_url}/api/v2/engagements/"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            engagements = response.json()
            return engagements
        else:
            print(f"Failed to retrieve engagements. Status code: {response.status_code}")
            return None

    def get_findings_for_engagement(self, engagement_id):
        # Implement code to retrieve findings for a specific engagement
        pass

    def get_scanner_findings(self, scanner_id):
        # Implement code to retrieve findings for a specific scanner
        pass

    def analyze_data(self, data):
        # Implement your analysis logic here using pandas or other libraries
        pass

    def _make_request(self, method, url, verify=True, **kwargs):
        try:
            session = requests.Session()
            response = session.request(method=method, url=url, verify=verify, **kwargs)
            response.raise_for_status()  # Raises an HTTPError for non-2xx responses
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request:{e}")
            return None


