
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics 
from datetime import datetime
import locale

# Set the locale to the user's default locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')



# Register Times New Roman font
pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
pdfmetrics.registerFont(TTFont('TimesNewRoman-bold', 'timesbd.ttf'))
pdfmetrics.registerFont(TTFont('TimesNewRoman-bold-italic', 'timesbi.ttf'))
pdfmetrics.registerFont(TTFont('TimesNewRoman-italic', 'timesi.ttf'))


# Function to generate random products
def generate_random_products(order, name):
    products = []

    for index,p in enumerate(order[name]): 
        product = {
            "index":index +1,
            "name": p["sn"],
            "description": f" {p['sn']} - {p['item']}",
            "quantity": p["qty"],
            "price": p["price"],
            "subtotal": p["subtotal"],
        }
         
        products.append(product)
    return products


    
def drawFirstTable(c,size,tableData,width,height, count, subtotal,discount,shipping, name="", dark=False,quote=False, fees = 0): 
    
    table = Table(tableData , colWidths = [50,220, 50, 100, 100], hAlign='LEFT', repeatRows=1)
    
    if dark:
        colours = colors.lightsteelblue
    else:
        colours = colors.lightgoldenrodyellow

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colours),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))

    offset = -50
    
    table.wrapOn(c, width - 100, height - 250)
    table.drawOn(c, 50, (height - 270 - (size * 20)) + offset) 

    offset -= 50

    if count <= 10:   
        c.setFont("TimesNewRoman", 10)
        c.drawString(width - 160, (height - 250 - (size * 20)) + offset, f"Sub-Total: {locale.currency(subtotal, grouping=True)}")
        c.drawString(width - 160, (height - 260 - (size * 20)) + offset, f"Discount  : {locale.currency(discount, grouping=True)}")
        c.drawString(width - 160, (height - 270 - (size * 20)) + offset, f"Fees         : {locale.currency(fees, grouping=True)}")
        c.drawString(width - 160, (height - 280 - (size * 20)) + offset, f"Shipping  : {locale.currency(shipping, grouping=True)}")
        c.setFont("TimesNewRoman-bold", 16)
        c.drawString(width - 160, (height - 300 - (size * 20)) + offset, f"Total: {locale.currency((subtotal + shipping + fees) - discount, grouping=True)}")
 
        # Footer
        footer(c,size, 180, quote=quote)
        
    elif count > 10 and count <= 17:
        
        offset -= 10
        c.setFont("TimesNewRoman", 10)
        c.drawString(width - 160, (height - 250 - (size * 20)) + offset, f"Sub-Total: {locale.currency(subtotal, grouping=True)}")
        c.drawString(width - 160, (height - 260 - (size * 20)) + offset, f"Discount  : {locale.currency(discount, grouping=True)}")
        c.drawString(width - 160, (height - 270 - (size * 20)) + offset, f"Fees         : {locale.currency(fees, grouping=True)}")
        c.drawString(width - 160, (height - 280 - (size * 20)) + offset, f"Shipping  : {locale.currency(shipping, grouping=True)}")
        c.setFont("TimesNewRoman-bold", 16)
        c.drawString(width - 160, (height - 300 - (size * 20)) + offset, f"Total: {locale.currency((subtotal + shipping + fees) - discount, grouping=True)}")
        c.showPage()
        # Footer
        footer(c,size, 750, quote=quote)
    
    elif count > 17 and count <= 20:
        c.showPage()
        offset += 650
        c.setFont("TimesNewRoman", 10)
        c.drawString(width - 160, (height - 250 - (size * 20)) + offset, f"Sub-Total: {locale.currency(subtotal, grouping=True)}")
        c.drawString(width - 160, (height - 260 - (size * 20)) + offset, f"Discount  : {locale.currency(discount, grouping=True)}")
        c.drawString(width - 160, (height - 270 - (size * 20)) + offset, f"Fees         : {locale.currency(fees, grouping=True)}")
        c.drawString(width - 160, (height - 280 - (size * 20)) + offset, f"Shipping  : {locale.currency(shipping, grouping=True)}")
        c.setFont("TimesNewRoman-bold", 16)
        c.drawString(width - 160, (height - 300 - (size * 20)) + offset, f"Total: {locale.currency((subtotal + shipping + fees) - discount, grouping=True)}")
     
        # Footer
        footer(c,size, 650, quote=quote)

def drawTable(c,size,tableData,width,height,dark=False ):  

    table = Table(tableData, colWidths=[50, 220, 50, 100, 100], hAlign='LEFT', repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    table.wrapOn(c, width - 100, height - 250)   

    offset = 0
    if size <= 18:
        offset = -40
    
    table.drawOn(c, 50, (height - size * 20) + offset ) 

def drawLastTable(c, size, tableData,width,height,subtotal,discount,shipping, name="", dark=False,quote=False, fees = 0): 
    table = Table(tableData , colWidths=[50, 220, 50, 100, 100], hAlign='LEFT', repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black)
    ]))

    offset = 0
    if size <= 18:
        offset = -40
        
    table.wrapOn(c, width - 100, height - 250)
    table.drawOn(c, 50, (height - size * 20) + offset)
    
    # print("SIZE",size)
    if size > 26:
        offset += 750
        c.showPage()         
        # Total
        c.setFont("TimesNewRoman", 10)
        c.drawString(width - 160,  offset -10 , f"Sub-Total: {locale.currency(subtotal, grouping=True)}")
        c.drawString(width - 160,  offset -20, f"Discount : {locale.currency(discount, grouping=True)}")
        c.drawString(width - 160,  offset -30, f"Fees        : {locale.currency(fees, grouping=True)}")
        c.drawString(width - 160,  offset -40, f"Shipping : {locale.currency(shipping, grouping=True)}")
        c.setFont("TimesNewRoman-bold", 16)
        c.drawString(width - 160,  offset -60, f"Total: {locale.currency((subtotal + shipping + fees) - discount, grouping=True)}")
        # c.showPage()    
        # Footer
        footer(c,size,  650, quote=quote )

    else:
        # Total 
        c.setFont("TimesNewRoman", 10)
        c.drawString(width - 160, (height - 50 - (size * 20)) + offset, f"Sub-Total: {locale.currency(subtotal, grouping=True)}")
        c.drawString(width - 160, (height - 60 - (size * 20)) + offset, f"Discount : {locale.currency(discount, grouping=True)}")
        c.drawString(width - 160, (height - 70 - (size * 20)) + offset, f"Fees        : {locale.currency(fees, grouping=True)}")
        c.drawString(width - 160, (height - 80 - (size * 20)) + offset, f"Shipping : {locale.currency(shipping, grouping=True)}")
        c.setFont("TimesNewRoman-bold", 16)
        c.drawString(width - 160, (height - 100 - (size * 20)) + offset, f"Total: {locale.currency((subtotal + shipping + fees) - discount, grouping=True)}")

        # Footer
        footer(c,size, (height - size * 20) + offset - 100, quote=quote)

def footer(c,size, height, quote=False ):
    offset = 50

    if quote:
        c.setFont("TimesNewRoman-bold", 16)
        c.drawString(50, height - offset +30 , "*** Note: The cost does not cover shipping fees.")
    
    # Draw footer
    c.setFont("TimesNewRoman-bold-italic", 16)
    c.drawString(50, height - offset , "Banking Information:")
    
    # Calculate text width
    text_width = c.stringWidth("Banking Information:")
    
    # Draw line beneath text
    y = height - offset - 3  
    c.line(50, y, 50 + text_width, y)

    offset += 30    

    c.setFont("TimesNewRoman-italic", 10)
    c.drawString(50, height - offset, "Payable to:               C'bean Inst. for Met and Hydrology")
    c.drawString(50, height - (12 * 1) - offset, "Account Holder:       C'bean Inst. for Met and Hydrology")
    c.drawString(50, height - (12 * 2) - offset, "Account Number:     1334332")
    c.drawString(50, height - (12 * 3) - offset, "Name of Bank:         First Caribbean International Bank")
    c.drawString(50, height - (12 * 4) - offset, "Address of Bank:      Broad Street, Bridgetown, Barbados")
    c.drawString(50, height - (12 * 5) - offset, "Bank (Swift) code:    FCIBBBBB")


def create_final_invoice(file_name,  order, name, fees = 0):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    products = generate_random_products(order, name)     

    if len(products) > 0:
        # Header
        c.setFont("TimesNewRoman-bold", 12)
        c.drawString(50, height - 50, "CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY")
        c.setFont("TimesNewRoman-bold-italic", 10)
        c.drawString(50, height - 65, "P.O. Box 130, Bridgetown, Barbados, W.I.")
        c.drawString(50, height - 80, "Tel: (246) 425-1362, 425-1363, 425-1365")
        c.drawString(50, height - 95, "Fax: (246) 424-4733 ")

        # Quotation
        c.setFont("Helvetica-Bold", 16) 
        if "_nci" in file_name:
             c.drawCentredString(width / 2, height - 150, "INVOICE (Pro-Bono Items)")
        else:
            c.drawCentredString(width / 2, height - 150, "INVOICE")

        # Draw order information
        c.setFont("TimesNewRoman-bold", 12)
        if "_nci" in file_name:
            c.drawString( width - 200, height - 170, f"Invoice#: {order['invoice']['number1']}")
        else:
            c.drawString( width - 200, height - 170, f"Invoice#: {order['invoice']['number']}")
        c.setFont("TimesNewRoman", 8)
        c.drawString( width - 200, height - 185, f"# {order['id']}")
        c.setFont("TimesNewRoman", 8)
        # date = datetime.strptime(order['ordered']['date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%a, %b %d,  %Y')
        date = order['invoice']['date'].strftime('%B %d,  %Y')

        c.setFont("TimesNewRoman", 12)
        c.drawString( 50, height - 185, f"Date: {date}")

        # Shipping
        c.setFont("TimesNewRoman-bold", 12)
        c.drawString( 50, height - 210, "Billed to: ")
        c.setFont("TimesNewRoman", 10)
        c.drawString( 110, height - 210, f"{order['billedto']['firstname']} {order['billedto']['lastname']}")
        c.drawString( 110, height - 222, f"{order['billedto']['office']}") 
        c.drawString( 110, height - 234, f"{order['billedto']['organization']}") 
        c.drawString( 110, height - 246, f"{order['billedto']['address']} ")
        c.drawString( 110, height - 258, f"{order['billedto']['city']} {order['billedto']['parish']}  {order['billedto']['zip']}")
        c.drawString( 110, height - 270, f"{order['billedto']['country']} ") 
        c.drawString( 110, height - 282, f"{order['billedto']['tel']} ") 
        

        size =  len(products)
                
        if size <= 12:
            s = [products] 
        else:
            s = [products[0:20]]
            a = [products[i:i+37] for i in range(20, size ,37)]
            s.extend(a) 
        
        tables = []

        # print("PAGES",len(s))
        
        for i,productss in enumerate(s):
            subTable = []
            if i == 0:
                subTable.extend([[ "Item","Description", "Quantity", "Price", "Amount (BBD)"]]) 

            for pro in productss: 
                subTable.extend([[ pro["index"],pro["description"], str(pro["quantity"]), f"${pro['price']}", f"${pro['subtotal']}"]])

            tables.extend([subTable])
            
        # Add shipping row to table
        # tables.extend([[ "Shipping", " ", f" ", f"${order['shipping']['cost']}"]])

        # Total
        subtotal = round(sum(product["subtotal"] for product in products), 2) 
        discount = 0
        shipping = order['shipping']['cost']

        if name == "products1":
            discount = subtotal
            shipping = order['shipping']['cost1']

        # Convert the number to a currency string
        # total = locale.currency(total, grouping=True)
        
        for page,table in enumerate(tables):
            count = len(s[page])
            if page == 0:
                #              
                drawFirstTable(c,count,table,width,height, size, subtotal=subtotal, discount=discount,shipping=shipping, name=name, dark=True, quote=False, fees = fees)
                
            elif page == len(tables) - 1:
                #             c, size, tableData,width,height,subtotal,discount,shipping, name="", dark=False,quote=False
                drawLastTable(c,count,table,width,height,subtotal=subtotal, discount=discount,shipping=shipping, name=name,dark=True,quote=False, fees = fees )     
                
            else:
                drawTable(c,count,table,width,height, True )

            c.showPage()
        
        c.save()


# Function to create the invoice
def create_quotation_one(file_name,  order, name, fees = 0):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    products = generate_random_products(order, name)

    if len(products) > 0:
        # Header
        c.setFont("TimesNewRoman-bold", 12)
        c.drawString(50, height - 50, "CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY")
        c.setFont("TimesNewRoman-bold-italic", 10)
        c.drawString(50, height - 65, "P.O. Box 130, Bridgetown, Barbados, W.I.")
        c.drawString(50, height - 80, "Tel: (246) 425-1362, 425-1363, 425-1365")
        c.drawString(50, height - 95, "Fax: (246) 424-4733 ")

        # Quotation
        c.setFont("Helvetica-Bold", 16) 
        if "_nci" in file_name:
             c.drawCentredString(width / 2, height - 150, "QUOTATION (Pro-Bono Items)")
        else:
            c.drawCentredString(width / 2, height - 150, "QUOTATION")

        # Draw order information
        c.setFont("TimesNewRoman-bold", 12)
        c.drawString( width - 200, height - 170, "Order:")
        c.setFont("TimesNewRoman", 8)
        c.drawString( width - 200, height - 185, f"# {order['id']}")
        c.setFont("TimesNewRoman", 8)
        # date = datetime.strptime(order['ordered']['date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%a, %b %d,  %Y')
        date = order['ordered'].strftime('%a, %b %d,  %Y')
        
        c.setFont("TimesNewRoman", 12)
        c.drawString( 50, height - 185, f"Date: {date}")

        # Shipping
        c.setFont("TimesNewRoman-bold", 10)
        c.drawString( 50, height - 210, "Billed to: ")
        c.setFont("TimesNewRoman", 10)
        c.drawString( 110, height - 210, f"{order['billedto']['firstname']} {order['billedto']['lastname']}")
        c.drawString( 110, height - 220, f"{order['billedto']['office']}")
        c.drawString( 110, height - 230, f"{order['billedto']['organization']} ")
        c.drawString( 110, height - 240, f"{order['billedto']['email']} ")
        c.drawString( 110, height - 250, f"{order['billedto']['address']} ")
        c.drawString( 110, height - 260, f"{order['billedto']['city']} {order['billedto']['parish']}  {order['billedto']['zip']}")
        c.drawString( 110, height - 270, f"{order['billedto']['country']} ")
        c.drawString( 110, height - 280, f"{order['billedto']['tel']} ")
        

        size =  len(products)
                
        if size <= 12:
            s = [products] 
        else:
            s = [products[0:20]]
            a = [products[i:i+37] for i in range(20, size ,37)]
            s.extend(a) 
        
        tables = []
        
        for i,productss in enumerate(s):
            subTable = []
            if i == 0:
                subTable.extend([[ "Item","Description", "Quantity", "Price", "Amount (BBD)"]]) 

            for pro in productss: 
                subTable.extend([[ pro["index"],pro["description"], str(pro["quantity"]), f"${pro['price']}", f"${pro['subtotal']}"]])

            tables.extend([subTable])
            
    

        # Total 
        subtotal = round(sum(product["subtotal"] for product in products), 2) 
        discount = 0
        shipping = 0

        if name == "products1":
            discount = subtotal

        # Convert the number to a currency string
        # total = locale.currency(total, grouping=True)
        
        for page,table in enumerate(tables):
            count = len(s[page])
            if page == 0:
                drawFirstTable(c,count,table,width,height, size, subtotal=subtotal, discount=discount,shipping=shipping, name=name, dark=False, quote=True, fees = fees )
                
            elif page == len(tables) - 1:
                drawLastTable(c,count,table,width,height,subtotal=subtotal, discount=discount,shipping=shipping, name=name,dark=False,quote=True, fees = fees )            
                
            else:
                drawTable(c,count,table,width,height )

            c.showPage()
        
        c.save()

def create_quotation(file_name,  order, fees = 0):     
     create_quotation_one(file_name,  order, "products", fees = fees)

     if len(order['ncicart']) > 0:
        name = file_name.split(".")[0]
        create_quotation_one(name+"_nci.pdf",  order, "products1", fees = fees)

def create_invoice(file_name,  order, fees = 0):     
     create_final_invoice(file_name,  order, "products", fees = fees)

     if len(order['ncicart']) > 0:
        name = file_name.split(".")[0]
        create_final_invoice(name+"_nci.pdf",  order, "products1", fees = fees)
     
def create_fileNotFound(file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Message
    c.setFont("Helvetica-Bold", 16) 
    c.drawCentredString(width / 2, height / 2, "File Not found") 
    c.save()


def create_ci_one(file_name,  order, name, fees = 0):
    # Commercial Invoice
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    products = generate_random_products(order, name)

    if len(products) > 0:
        # Header
        c.setFont("TimesNewRoman-bold", 12)
        c.drawString(50, height - 50, "CARIBBEAN INSTITUTE FOR METEOROLOGY AND HYDROLOGY")
        c.setFont("TimesNewRoman-bold-italic", 10)
        c.drawString(50, height - 65, "P.O. Box 130, Bridgetown, Barbados, W.I.")
        c.drawString(50, height - 80, "Tel: (246) 425-1362, 425-1363, 425-1365")
        c.drawString(50, height - 95, "Fax: (246) 424-4733 ")

        # Quotation
        c.setFont("Helvetica-Bold", 16) 
        if "_nci" in file_name:
             c.drawCentredString(width / 2, height - 130, "Commercial Invoice")
             c.drawCentredString(width / 2, height - 150, "(Pro-Bono Items)")
        else:
            c.drawCentredString(width / 2, height - 150, "Commercial Invoice")

        # Draw order information
        c.setFont("TimesNewRoman-bold", 10)
        if "_nci" in file_name:
            c.drawString( width - 200, height - 200, f"Commercial Invoice #: {order['invoice']['number4']}")
        else:
            c.drawString( width - 200, height - 200, f"Commercial Invoice #: {order['invoice']['number3']}")

        c.setFont("TimesNewRoman-bold", 12)
        c.drawString( width - 200, height - 170, "Order:")
        c.setFont("TimesNewRoman", 8)
        c.drawString( width - 200, height - 185, f"# {order['id']}")
        c.setFont("TimesNewRoman", 8)
        # date = datetime.strptime(order['ordered']['date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%a, %b %d,  %Y')
        date = order['ordered'].strftime('%a, %b %d,  %Y')
        
        c.setFont("TimesNewRoman", 12)
        c.drawString( 50, height - 185, f"Date: {date}")

        # Shipping
        c.setFont("TimesNewRoman-bold", 10)
        c.drawString( 50, height - 210, "To: ")
        c.setFont("TimesNewRoman", 10)
        c.drawString( 80, height - 210, f"{order['billedto']['firstname']} {order['billedto']['lastname']}")
        c.drawString( 80, height - 222, f"{order['billedto']['organization']} ")
        c.drawString( 80, height - 234, f"{order['billedto']['email']} ")
        c.drawString( 80, height - 246, f"{order['billedto']['address']} ")
        c.drawString( 80, height - 258, f"{order['billedto']['city']} {order['billedto']['parish']}  {order['billedto']['zip']}")
        c.drawString( 80, height - 270, f"{order['billedto']['country']} ")
        c.drawString( 80, height - 282, f"{order['billedto']['tel']} ")
        

        size =  len(products)
                
        if size <= 12:
            s = [products] 
        else:
            s = [products[0:20]]
            a = [products[i:i+37] for i in range(20, size ,37)]
            s.extend(a) 
        
        tables = []
        
        for i,productss in enumerate(s):
            subTable = []
            if i == 0:
                subTable.extend([[ "Item","Description", "Quantity", "Price", "Amount (BBD)"]]) 

            for pro in productss: 
                subTable.extend([[ pro["index"],pro["description"], str(pro["quantity"]), f"${pro['price']}", f"${pro['subtotal']}"]])

            tables.extend([subTable])
            
    

        # Total 
        subtotal = round(sum(product["subtotal"] for product in products), 2) 
        discount = 0
        shipping = 0

        if name == "products1":
            discount = subtotal

        # Convert the number to a currency string
        # total = locale.currency(total, grouping=True)
        
        for page,table in enumerate(tables):
            count = len(s[page])
            if page == 0:
                drawFirstTable(c,count,table,width,height, size, subtotal=subtotal, discount=discount,shipping=shipping, name=name, dark=False, quote=True, fees = fees )
                
            elif page == len(tables) - 1:
                drawLastTable(c,count,table,width,height,subtotal=subtotal, discount=discount,shipping=shipping, name=name,dark=False,quote=True, fees = fees )            
                
            else:
                drawTable(c,count,table,width,height )

            c.showPage()
        
        c.save()

def create_comm_inv(file_name,  order, fees = 0):  
       
     create_ci_one(file_name,  order, "products", fees = fees)

     if len(order['ncicart']) > 0:   
        name = file_name.split(".")[0]     
        create_ci_one(name+"_nci.pdf",  order, "products1", fees = fees)

order =   {
  "customer": "ACC1eaa0653f9b470176d0c4cb5d0e5ac25",
  "ncicart": [
    { "id": "METc01f88b6d134abf986fbe32b3c200997", "count": 2, "cost": 61.41, "picked": [] },
    { "id": "SUPPaeb054f649e35cc59fc0f0dc171718b3", "count": 2, "cost": 28.45, "picked": [] },
  ],
  "billedto": {
    "firstname": "Tajay",
    "lastname": "Edwards",
    "organization": "CIMH",
    "email": "testemail@gmail.com",
    "address": "241 Delavega City",
    "city": "Spanish Town",
    "parish": "St Catherine",
    "tel": "5166566565665",
    "country": "Jamaica",
    "zip": "1876"
  },
    "billedto": {
    "firstname": "Tajay",
    "lastname": "Edwards",
    "organization": "CIMH",
    "email": "testemail@gmail.com",
    "address": "241 Delavega City",
    "city": "Spanish Town",
    "parish": "St Catherine",
    "tel": "5166566565665",
    "country": "Jamaica",
    "zip": "1876"
  },
  "total": 495.26,
  "shippingestimate": 0,
  "firstname": "Naruto",
  "lastname": "Uzumaki",
  "id": "ORD351915ae482ae96920de1f25980f241d",
  "ordered": datetime.strptime("2024-08-13T20:44:03",'%Y-%m-%dT%H:%M:%S'),
  "files": [],
  "shipping": {
    "date": "",
    "method": "",
    "tracking": "",
    "cost": 1000,
    "cost1": 150
  },
  "invoice": {
    "number": "001",
    "number1": "002",
    "number3": "003",
    "number4": "004",
    "date": datetime.strptime("2024-02-16T12:25:37",'%Y-%m-%dT%H:%M:%S')
  },
  "complete": False,
  "paid": False,
  "cancelled": False,
  "products": [
    { "item": "Handcrafted Shoes", "price": 85, "sn": "352593", "qty": 1, "subtotal": 85 },
    # { "item": "Durable Chair", "price": 59.1, "sn": "907317", "qty": 1, "subtotal": 59.1 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Handcrafted Shoes", "price": 85, "sn": "352593", "qty": 1, "subtotal": 85 },
    # { "item": "Durable Chair", "price": 59.1, "sn": "907317", "qty": 1, "subtotal": 59.1 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Handcrafted Shoes", "price": 85, "sn": "352593", "qty": 1, "subtotal": 85 },
    # { "item": "Durable Chair", "price": 59.1, "sn": "907317", "qty": 1, "subtotal": 59.1 }, 
    # { "item": "Handcrafted Shoes", "price": 85, "sn": "352593", "qty": 1, "subtotal": 85 },
    # { "item": "Durable Chair", "price": 59.1, "sn": "907317", "qty": 1, "subtotal": 59.1 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },

    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },

    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    # { "item": "Stylish Umbrella", "price": 18.73, "sn": "201067", "qty": 2, "subtotal": 37.46 },
    # { "item": "Affordable Chair", "price": 87.36, "sn": "131094", "qty": 2, "subtotal": 174.72 },
    # { "item": "Futuristic Shoes", "price": 69.49, "sn": "400694", "qty": 2, "subtotal": 138.98 },
    

  ],
  "products1": [
    { "item": "Innovative Wallet", "price": 61.41, "sn": "148111", "qty": 2, "subtotal": 122.82 },
    { "item": "Innovative Painting", "price": 28.45, "sn": "516128", "qty": 2, "subtotal": 56.9 }
  ]
}


def maintainAuth():
        # CONTROLS MQTT CONNECTION TO CONTROLBOARD
        from time import time, sleep   
        count = 0

        while True:
            print("COUNT ",count)
            count += 1
            sleep(1)



def maintainFedExAuthToken():        
        from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor 

        # with ThreadPoolExecutor(max_workers=3) as executor: # RUN USING THREADING
        with ProcessPoolExecutor(max_workers=7) as executor: # DO NOT RUN USING MULTIPROCESSING, SPECIAL QUEUES ARE NEED OTHERWISE CODE WILL FAIL
                future0  = executor.submit(maintainAuth) 

                if(future0.running()):
                        print(" Task 0 running")
           


if __name__ == '__main__':
    # Define invoice details
    file_name = "invoice.pdf" 
    fees = 40
    # Create the invoice
    # create_invoice(file_name, order, fees)
    create_comm_inv(file_name, order, fees)
    # create_quotation(file_name,  order, fees)
 
 
