import logging
import os
import warnings

import numpy as np
import pandas as pd
import requests
from config import SUCCESS_STATUS_CODE
from dotenv import find_dotenv, load_dotenv
from packageurl import PackageURL


class DependencyTrack:
    # Set Dependency Track instance base URL
    DEPENDENCY_TRACK_BASE_URL = "https://dependency-track.poc.roche.com"  
    # Set API version
    API_VERSION = "v1"  
    # Set the API URL of your Dependency Track instance 
    DEPENDENCY_TRACK_API_URL = f"{DEPENDENCY_TRACK_BASE_URL}/api/{API_VERSION}"

    def __init__(self):
        self.project_info = None

        # Load API_KEY
        load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=False))

        # Set API key
        self.API_KEY = os.getenv('DEPENDENCY_TRACK_API_KEY')

        # Add list with all scanner names
        self.scanner_names = ['gitlab_cont', 
                              'jfrog_advanced_security_cont', 
                              'jfrog_cont', 
                              'syft_cont', 'trivy_cont']

        self._get_all_projects()
        if self.project_info is None:
            print("Initialization failed: Project information not available")   
    
    def _get_all_projects(self):
        # sourcery skip: extract-method, remove-unnecessary-else
        # Code to retrieve project names and UUIDs
        # Store the data in self.projects attribute
        """
        Retrieve all projects and their versions from the Dependency Track API.
    
        Returns:
            pandas.DataFrame or None:
                A DataFrame containing project names, versions, and UUIDs,
                or None if the request fails.
        Raises:
            None
    
        Example:
            >>> api_key = "your_api_key"
            >>> base_url = "https://dependency-track.example.com/api/v1/"
            >>> df = get_all_projects(api_key, base_url)
        
        DataFrame project_info with project information (Name, Version, UUID) or None
        is stored
    
        Notes:
            The `SUCCESS_STATUS_CODE` constant represents the HTTP status code that 
            indicates a successful response from the Dependency Track API. By default, 
            it is set to 200.
        """  
        # Set the headers with the API key
        headers =  {                     
            "accept": "application/json",
            "X-Api-Key": self.API_KEY
        }      

        # Make the request to get all projects
        url = f"{self.DEPENDENCY_TRACK_API_URL}/project"
        response = self._make_request(method='GET', 
                                      url=url, 
                                      verify=False, 
                                      headers=headers)

        # Check the response status
        if response is not None and response.status_code == SUCCESS_STATUS_CODE:
            projects = response.json()
            data = {
                "Name": [],
                "Version": [],
                "UUID": []
            }
            for project in projects:
                data["Name"].append(project["name"])
                # Check if the "version" key exists in the current project dictionary
                version = project.get("version", "None")  # Use "None" as the default value
                data["Version"].append(version)
                data["UUID"].append(project["uuid"])                                                                                                

            self.project_info = pd.DataFrame(data)
            return pd.DataFrame(data)
        else:
            logging.error("Failed to get projects.")
            return None
    
    def _get_project_data(self, project_name, project_version:None):
        # Code to retrieve project data using project_name and scanner_names
        # Use self.project_info to access the project names and UUIDs
        """
        Retrieves and combines data frames for a given project name and list of scanner 
        names.

        Parameters:
            project_name (str): The name of the project.
            scanner_names (list): A list of scanner names.

        Returns:
            pandas.DataFrame: The combined data frame containing the values of all 
                              projects.

        Raises:
            IndexError: If the UUID for a scanner project is not found in the 
                        projects_df.

        Example:
            combined_df = get_project_data('project_name', ['scanner1', 'scanner2'])
        """

        # Add list with UUID to every scanner project for the current project_name
        project_list = [f"{project_name}_{scanner_name}" for scanner_name in self.scanner_names]  # noqa: E501

        if self.project_info is not None:
            project_info_df = self.project_info

            if project_version is None:
                mask = project_info_df['Name'].isin(project_list) 
            else:
                mask = ((project_info_df['Name'].isin(project_list)) & 
                        (project_info_df['Version'] == str(project_version)))
            
            matching_rows = project_info_df[mask]
            nr, _ = matching_rows.shape
            if nr > 0:
                uuids = matching_rows['UUID'].tolist()
            else:
                print(f"Error: no project with {project_name} and version {project_version} known")
                return

            try:
                # Create a list of the data frames of every scanner
                data_frames = [self._get_project_components(uuid)  
                               for uuid in uuids]
            except Exception as e:
                # Handle the exception here
                logging.error(f"An error occurred: {e}")
                return

            # Add scanner name and UUID columns to each data frame
            for i, df in enumerate(data_frames):
                if df is not None:
                    df['scanner_name'] = self.scanner_names[i]
                    df['UUID'] = uuids[i]
                else:
                    message = (
                        f"No component information available for project {project_name} "
                        f"with project uuid {uuids[i]}")
                    print(message)
    
            # Filter out None values from the list
            filtered_data_frames = [df for df in data_frames if df is not None]

            # Concatenate the data frames into one
            if filtered_data_frames is not None:
                return pd.concat(filtered_data_frames, ignore_index=True)
        else:
            print("Project info is not available.")
            logging.error("Project info is not available.")
            return None
   
    def _get_project_components(self, project_uuid):
        # Code to retrieve SBOM for a project with the given UUID

        """
        Retrieve all component information from the SBOM of a specific project.
    
        Args:
            project_uuid (str): The UUID of the project.
            api_key (str): The API key for authentication with the Dependency Track API.
            base_url (str): The base URL of the Dependency Track API.
    
        Returns:
            pd.DataFrame or None:
                A DataFrame containing component names, versions, and UUIDs,
                or None if the request fails.

        Raises:
            None
    
        Example:
            >>> api_key = "your_api_key"
            >>> base_url = "https://dependency-track.example.com/api/v1/"
            >>> df = get_project_SBOM_components("your_project_uuid", api_key, base_url)
        
        DataFrame with component information or None
        """

        # Set the headers with the API key
        headers = {
                    "accept": "application/vnd.cyclonedx+xml",
                    "X-Api-Key": self.API_KEY
                    }
        
        # Make the API request to retrieve the SBOM data
        url = f"{self.DEPENDENCY_TRACK_API_URL}/bom/cyclonedx/project/{project_uuid}"  
        response = self._make_request(method='GET', 
                                      url=url, 
                                      verify=False, 
                                      headers=headers)

        # Check the response status
        if (response is not None and response.status_code is not None 
            and response.status_code == SUCCESS_STATUS_CODE):
     
            sbom_data = response.json()
            try:
                # Process the SBOM data as 
                df = pd.DataFrame(sbom_data['components'])
            except KeyError:
                df = None
            return df
        else:
            print("Error: Failed to retrieve SBOM data.")
            return None

    def collect_all_scanner_data(self, project_name, project_version:None):
        # Code to collect all scanner data for a project
        # Use self.get_project_data and self.get_project_components

        def extract_value(x, key):
            if isinstance(x, list) and len(x) > 0 and isinstance(x[0], dict):
                return x[0][key]
            else:
                return np.nan

        try:
            # get data of all scanners in 'scanner_names' for project 'project_name'
            project_data_df = self._get_project_data(project_name, project_version)
        except Exception as e:
            # Handle the exception here
            project_data_df = None
            logging.error(f"An error occurred loading the scanner data: {e}")

        # Create list with scanner index.    
        if (project_data_df is not None and isinstance(project_data_df, pd.DataFrame)
            and self.project_info is not None):
            scanner_masks = [project_data_df['scanner_name'] == scanner_name 
                             for scanner_name in self.scanner_names]

            # Create a data frame 'data_df' with all scanner data for one project 
            data_df = {
                name: project_data_df.loc[mask, ['scanner_name', 'name', 'version', 
                                                   'purl', 'bom-ref', 'hashes']] 
                                                   for name, mask in 
                                                   zip(self.scanner_names, 
                                                       scanner_masks)}

            # Select data from scanners and add dot df_list (df_list[0] are all data of 
            # interest from scanner scanner_names[0]
            scanner_data = {}
            for scanner_name in self.scanner_names:
                # Select data and reset index
                df = data_df[scanner_name]
                df.reset_index(drop=True, inplace=True)

                # Evaluate hash_algo and hash_sum
                df['hash_sum'] = df['hashes'].apply(lambda x: extract_value(x, 'content'))
                df['hash_algo'] = df['hashes'].apply(lambda x: extract_value(x, 'alg'))

                # Apply the parse_url function to each element of the 'purl' column
                df_parsed = df['purl'].apply(self._parse_purl)

                # Convert the parsed_data Series of dictionaries into a DataFrame
                df_parsed_df = pd.DataFrame(df_parsed.to_list())

                # Concatenate the parsed_df DataFrame with the original df DataFrame
                df = pd.concat([df, df_parsed_df], axis=1)

                # Add data frame for scanner_name to dictionary
                scanner_data[scanner_name] = df

            return scanner_data
        else:
            if project_data_df is None:
                # project_data_df could not be pulled
                print("Data frame project_data_df is not available")
                logging.error("Data frame project_data_df is not available")
                
            elif isinstance(project_data_df, pd.DataFrame):
                # project_info not initialized
                print("Variable project_data_df is not a data frame")
                logging.error("Variable project_data_df is not a data frame")
            else: 
                # project_info not initialized
                print("Data frame project_info is not initialized")
                logging.error("Data frame project_info is not initialized")
    
    def _parse_purl(self, purl_string):
        # Code to parse the purl and extract information
    
        try:
            purl = PackageURL.from_string(purl_string)
            purl_components = purl.to_dict()
        except Exception as e:
        # Handle any exceptions that occurred during parsing
            warnings.warn(f"Error parsing PURL: {e}")
            purl_components = {
                'type': None,
                'namespace': None,
                'name': None,
                'version': None,
                'qualifiers': None,
                'subpath': None
            }  

        return {f'p_{key}': value for key, value in purl_components.items()}

    def _make_request(self, method, url, verify=True, **kwargs):
        try:
            session = requests.Session()
            response = session.request(method=method, url=url, verify=verify, **kwargs)
            response.raise_for_status()  # Raises an HTTPError for non-2xx responses
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request:{e}")
            return None
