import uuid
from fpdf import FPDF

# Color Constants
WHITE = 'FFFFFF'
BLACK = '000000'
YELLOW = 'FFFF00'
RED = '253-0-0'
MOMO_DARK = '29-29-27'
MOMO_ORANGE = '253-193-0'

# Input
numberOfSets = 1 # Each set contains 12 cards an creates two DinA4 pages (front and back side)
pdfFileName = "out/Momo-FanCards_1_Standard.pdf" #"Momo-FanCards_120_Premium.pdf"
guidsFileName = "out/Momo-FanCards_1_Standard.txt" #"Momo-FanCards_120_Premium.txt"
frontImg = "Momo-FanCard-Front_744x744.png"
imageFormat = "PNG"
qrForegroundColor = MOMO_DARK
qrBackgroundColor = MOMO_ORANGE #RED
contentTemplate = "https://momo-music.de/fan?id={}"
qrUriTemplate = "https://api.qrserver.com/v1/create-qr-code?data={}&size=238x238&bgcolor={}&color={}"

# Dimensions
cardsPerRow = 3
rowsPerPage = 4
cardEdgeMillis = 63 # The width and height of each card
qrImgScale = 0.8 # The scaling factor of the QR-Code in relation to cardEdgeMillis
cuttingLineMillis = 0.25
dinA4WidthMillis = 210
dinA4HeightMillis = 297
marginLeftMillis = (dinA4WidthMillis - cardsPerRow*cardEdgeMillis - (cardsPerRow-1)*cuttingLineMillis) / 2
marginTopMillis = (dinA4HeightMillis - rowsPerPage*cardEdgeMillis - (rowsPerPage-1)*cuttingLineMillis) / 2

# Open file to write generated GUIDs to
guidsFile = open(guidsFileName,"w+")

# Generate PDF
pdf = FPDF()
for setNumber in range(numberOfSets):
    # Create front page
    pdf.add_page()
    for row in range(rowsPerPage):
        for col in range(cardsPerRow):
            pdf.image(frontImg, marginLeftMillis+(cuttingLineMillis+cardEdgeMillis)*col, marginTopMillis+(cuttingLineMillis+cardEdgeMillis)*row, cardEdgeMillis, cardEdgeMillis, imageFormat)    
    
    # Create back page
    pdf.add_page()
    for row in range(rowsPerPage):
        for col in range(cardsPerRow):
            fanId = uuid.uuid4()
            fanUri = contentTemplate.format(fanId)
            print(fanUri)
            qrUri = qrUriTemplate.format(fanUri, qrBackgroundColor, qrForegroundColor)
            x = marginLeftMillis+(cardEdgeMillis*(1-qrImgScale)/2)+(cuttingLineMillis+cardEdgeMillis)*col
            y = marginTopMillis+(cardEdgeMillis*(1-qrImgScale)/2)+(cuttingLineMillis+cardEdgeMillis)*row
            pdf.image(qrUri, x, y, cardEdgeMillis*qrImgScale, cardEdgeMillis*qrImgScale, imageFormat, qrUri)
            guidsFile.write("{}\n".format(fanId))

# Write PDF file
pdf.output(pdfFileName, 'F')
guidsFile.close()