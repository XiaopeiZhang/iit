import urllib, urllib2, math, os, webbrowser, json, io
from PIL import Image

MyKey = "AuKLhlR62LeHSNguaMCv_L2qCv1qX0bsvTjNJsbnTrI9FS7IPymuLFR8l8EfGV1E"
MetadataPath = "http://dev.virtualearth.net/REST/v1/Imagery/Metadata/Aerial"
EarthRadius = 6378137
MinLatitude = -85.05112878
MaxLatitude = 85.05112878
MinLongitude = -180
MaxLongitude = 180

def clip(n, minV, maxV):
    return min(max(n, minV), maxV)

def mapSize(level):
    return 256 << level

def latLongToPixelXY(lat, lon, level):
    lat = clip(lat, MinLatitude, MaxLatitude)
    lon = clip(lon, MinLongitude, MaxLongitude)
    x = (lon + 180.0) / 360
    sinLat = math.sin(lat * math.pi / 180)
    y = 0.5 - math.log((1 + sinLat) / (1 - sinLat)) / (4 * math.pi)
    map_size = mapSize(level)
    pX = clip(x * map_size + 0.5, 0, map_size - 1)
    pY = clip(y * map_size + 0.5, 0, map_size - 1)
    return int(pX), int(pY)

def pixelXYToTileXY(x, y):
    return x / 256, y / 256

def tileXYToQuadKey(x, y, z):
    quadKey = ''
    for i in range(z, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if(x & mask) != 0:
            digit += 1
        if(y & mask) != 0:
            digit += 2
        quadKey += str(digit)
    return quadKey

def getTileURL(x, y, z):
    quadKey = tileXYToQuadKey(x, y, z)
    return "http://ecn.t3.tiles.virtualearth.net/tiles/a" + quadKey+ ".jpeg?g=5148&mkt=en-us"

def getTileImage(x, y, z):
    url = getTileURL(x, y, z)
    saveDir = os.path.join(os.getcwd(), "pics")
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    urllib.urlretrieve(url, os.path.join(saveDir, "tX" + str(x) + "_tY" + str(y) + "_zoomLevel" + str(z) + ".jpeg"))
    #webbrowser.open(url)

def getMaxZoom2(left, top, right, bottom):
    print "max"
    zoom1 = 1
    while zoom1 < 22:
        url = "%s/%s,%s?zl=%s&key=%s" % (MetadataPath, top, left, zoom1, MyKey)
        response = json.loads(urllib2.urlopen(url).read())
        print response
        if "errorDetails" not in response:
            data = response["resourceSets"][0]["resources"][0]
            if data["vintageEnd"] == None:
                zoom1 -= 1
                break
        else:
            print("error")
        zoom1 += 1
    zoom1 = min(zoom1, 21)
    zoom2 = 1
    while zoom2 < 22:
        url = "%s/%s,%s?zl=%s&key=%s" % (MetadataPath, bottom, right, zoom2, MyKey)
        response = json.loads(urllib2.urlopen(url).read())
        print response
        if "errorDetails" not in response:
            data = response["resourceSets"][0]["resources"][0]
            if data["vintageEnd"] == None:
                zoom2 -= 1
                break
        else:
            print("error")
        zoom2 += 1
    zoom2 = min(zoom2, 21)
    return min(zoom1, zoom2)

def getMaxZoom1(left, top, right, bottom):
    print "max"
    centerX = (left + right) / 2
    centerY = (top + bottom) / 2
    print centerX, centerY
    zoom = 21
    while True:
        url = "%s/%s,%s?zl=%s&key=%s" % (MetadataPath, centerY, centerX, zoom, MyKey)
        response = json.loads(urllib2.urlopen(url).read())
        print response
        if "errorDetails" not in response:
            data = response["resourceSets"][0]["resources"][0]
            if data["vintageEnd"]: break
        else:
            print("error")
        zoom -= 1
    return zoom

def getMaxZoom(left, top, right, bottom):
    print "max"
    centerX = (left + right) / 2
    centerY = (top + bottom) / 2
    print centerX, centerY
    zoom = 1
    while zoom < 22:
        url = "%s/%s,%s?zl=%s&key=%s" % (MetadataPath, centerY, centerX, zoom, MyKey)
        response = json.loads(urllib2.urlopen(url).read())
        print response
        if "errorDetails" not in response:
            data = response["resourceSets"][0]["resources"][0]
            if data["vintageEnd"] == None:
                zoom -= 1
                break
        else:
            print("error")
        zoom += 1
    zoom = min(zoom, 21)
    return zoom

def getPicsWithBoundingBox(top, left, bottom, right):
    maxLevel = getMaxZoom2(left, top, right, bottom)
    print maxLevel
    pX1, pY1 = latLongToPixelXY(top, left, maxLevel)
    print "1"
    print pX1, pY1
    tX1, tY1 = pixelXYToTileXY(pX1, pY1)
    print tX1, tY1
    print pX1%256, pY1%256
    pX2, pY2 = latLongToPixelXY(bottom, right, maxLevel)
    pX2, pY2 = pX2 + 1, pY2 + 1
    print "2"
    print pX2, pY2
    tX2, tY2 = pixelXYToTileXY(pX2, pY2)
    print tX2, tY2
    print pX2%256, pY2%256
    bigImage = Image.new("RGBA", ((tX2 + 1 - tX1) * 256, (tY2 + 1 - tY1) * 256), (0,0,0,0))
    for i in range(tX1, tX2 + 1):
        for j in range(tY1, tY2 + 1):
            tileURL = getTileURL(i, j, maxLevel)
            getTileImage(i, j, maxLevel)
            tile = urllib2.urlopen(tileURL).read()
            image = Image.open(io.BytesIO(tile))
            bigImage.paste(image, ((i - tX1) * 256, (j - tY1) * 256))
    bigImageName = "tX" + str(tX1) + "-" + str(tX2) + "_tY" + str(tY1) + "-" + str(tY2) + "_zoomLevel" + str(maxLevel) + ".jpeg"
    bigImage.save(bigImageName)
    im = Image.open(bigImageName)
    print pX1 % 256, pY1 % 256, pX2 - tX1 * 256, pY2 - tY1 * 256
    region = im.crop([pX1 % 256, pY1 % 256, pX2 - tX1 * 256, pY2 - tY1 * 256])
    region.save("crop_" + bigImageName)

#webbrowser.open("http://ecn.t3.tiles.virtualearth.net/tiles/a2.jpeg?g=5148&mkt=en-us")
getPicsWithBoundingBox(41.838199, -87.629596, 41.834726, -87.625123)