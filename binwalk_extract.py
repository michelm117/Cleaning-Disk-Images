import binwalk

img = "img/puppy/bachelor_os.img"
for module in binwalk.scan(img, signature=True, quiet=True, extract=True):
    print("%s Results:" % module.name)
    for result in module.results:
        print("\t%s    0x%.8X    %s" %
              (result.file.path, result.offset, result.description))
        if result.file.path in module.extractor.output:
            # These are files that binwalk carved out of the original firmware image, a la dd
            if result.offset in module.extractor.output[result.file.path].carved:
                print("Carved data from offset 0x%X to %s" % (
                    result.offset, module.extractor.output[result.file.path].carved[result.offset]))
