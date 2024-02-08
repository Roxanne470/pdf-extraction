from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import ExtractRenditionsElementType

import sys, time
import os.path
import zipfile
import json


def extracting(split_folder, output_folder):

    files = os.listdir(split_folder)
    files = [file for file in files if file!= ".DS_Store"]

    for file in files:

        pages = os.listdir(os.path.join(split_folder, file))

        for page in pages:

            input_file = os.path.join(split_folder, file, page)  # input_pdf = "split_pages/Q2_2023_Air_Canada_MDA.pdf/20.pdf"
            file_name = file.split(".")[0]
            page_no = page.split(".")[0]
            output_file = os.path.join(output_folder, file_name + "_P" + page_no + ".zip")  # zip_file = "Q2_2023_Air_Canada_MDA_P20.zip"
            print(output_file)

            if os.path.isfile(output_file):
                os.remove(output_file)

            #Set operation input from a source file.
            source = FileRef.create_from_local_file(input_file)
            extract_pdf_operation.set_input(source)

            #Build ExtractPDF options and set them into the operation
            extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
                .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
                .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
                .build()
            extract_pdf_operation.set_options(extract_pdf_options)

            #Execute the operation.
            result: FileRef = extract_pdf_operation.execute(execution_context)

            #Save the result to the specified location.
            result.save_as(output_file)

# archive = zipfile.ZipFile(zip_file, 'r')
# jsonentry = archive.open('structuredData.json')
# jsondata = jsonentry.read()
# data = json.loads(jsondata)

# for element in data["elements"]:
#     if(element["Path"].endswith("/H1")):
#         print(element["Text"])
if __name__ == "__main__":
    if len(sys.argv) != 3:
            print("Usage: python3 adobe_extract.py split_folder output_folder")
            sys.exit(1)

    #Initial setup, create credentials instance.
    credentials = Credentials.service_principal_credentials_builder() \
    .with_client_id("ec1faefa832c4f199c319eb1718ee03f") \
    .with_client_secret("p8e-3uUGcT2zbffCVnzGbsYa-2bBuCvJNoTm") \
    .build()

    #Create an ExecutionContext using credentials and create a new operation instance.
    execution_context = ExecutionContext.create(credentials)
    extract_pdf_operation = ExtractPDFOperation.create_new()

    split_folder = sys.argv[1]
    output_folder = sys.argv[2]

    start_time = time.time()

    extracting(split_folder, output_folder)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")