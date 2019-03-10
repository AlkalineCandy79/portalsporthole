## Portal's Porthole

This tiny python script is an ArcGIS Online or ArcGIS Portal Web Map REST Service interregator.  It was developed to quickly determine what REST services were being consumed for use within Web Maps.  OATH and SAML do not work here, so you will need a standard AGOL or Local Portal account to use this script.  Perhaps in the near future when Esri updates its Python library this option will be available...hopefully.

### Configuration

Where to configure.....(An area that I will make more intuitive later.)

```markdown
1)  gis = GIS("https://cobgis.maps.arcgis.com/","","") #non-saml or ADFS user name, #password
2)  search_results = gis.content.search(query="",item_type="Web Map",max_items=100000)
3)  itemURL = '=HYPERLINK("http://YOURPORTAL.maps.arcgis.com/home/item.html?id={0}","Launch Map")'.format(result.itemid)
```
### Support or Contact

This is provided as is and without warranty.  If you have any questions, please feel free to reach out to john@spence.dev.
