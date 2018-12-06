#VFmanglemapmask
This tool allows you to attempt to mangle, extract and list the heightmap and mask data in a VF bundle.
Parameters depend on the action. 

  * List 		- Lists available IDs, sizes and filenames of masks and maps
  * Extract	- Extracts all the heightmaps/mask into a directory
  * Replace	- Allows the replacement of a heightmap or mask

  *{List} [Bundle Source]
  *{Extract} [Bundle Source] [Extract-Directory]
  *{Replace} [Bundle Source] [Map-ID] [Replacement-File]

#Examples
##List
List simply lists the internal ID, file sizes and original filenames of heightmaps/masks
    >CLmanglehmaps.py list c:\Games\CardLife\Assets\bundles\terrain_bundle\
    ID                                      Size            Original Filename
    02a980cc-e8da-4adb-b063-af8db1dbbd79    16777216        C:\CardLife\Design\World\Biome_Forest\raw\all_exported.raw
    acd4722e-7eca-4a4e-8277-c236984017f2    16777216        C:\CardLife\Design\World\Biome_Forest\raw\beach.raw
    d77e0964-7f53-450a-9a07-b9acdf30f3e3    16777216        C:\CardLife\Design\World\Biome_Forest\raw\grass.raw
    d2b4e2a9-e834-455a-a363-69ff1885e03f    16777216        C:\CardLife\Design\World\Biome_Forest\raw\stone.raw
    08a645b4-d478-4a43-a515-709980b6f57e    16777216        C:\CardLife\Design\World\Biome_Forest\raw\dirt.raw
    d45c8b3b-7a3c-4e4a-a795-092d9afbda66    16777216        C:\CardLife\Design\World\Biome_Forest\raw\snow.raw
    b0ce8615-f79b-4ff6-83b5-dcef33bb5f5c    16777216        C:\CardLife\Design\World\Biome_Forest\raw\compact_stone.raw
    ac7156e0-7b70-4b48-bba0-cbd6f6f0c249    33554432        C:\CardLife\Design\World\Biome_Forest\raw\heightmap.raw
    8e1d7677-c859-41d1-9897-d995d4e8b07f    16777216        C:\CardLife\Design\World\Biome_Forest\raw\all_exported.raw

##Extract
Extract extracts all the heightmaps/masks into a target directory
    >CLmanglehmaps.py extract c:\Games\CardLife\Assets\bundles\terrain_bundle\ raw
    Extracting all_exported.raw (was C:\CardLife\Design\World\Biome_Forest\raw\all_exported.raw)
    Extracting beach.raw (was C:\CardLife\Design\World\Biome_Forest\raw\beach.raw)
    Extracting grass.raw (was C:\CardLife\Design\World\Biome_Forest\raw\grass.raw)
    Extracting stone.raw (was C:\CardLife\Design\World\Biome_Forest\raw\stone.raw)
    Extracting dirt.raw (was C:\CardLife\Design\World\Biome_Forest\raw\dirt.raw)
    Extracting snow.raw (was C:\CardLife\Design\World\Biome_Forest\raw\snow.raw)
    Extracting compact_stone.raw (was C:\CardLife\Design\World\Biome_Forest\raw\compact_stone.raw)
    Extracting heightmap.raw (was C:\CardLife\Design\World\Biome_Forest\raw\heightmap.raw)
    Extracting all_exported.raw (was C:\CardLife\Design\World\Biome_Forest\raw\all_exported.raw)

##Replace
Replace allows the replacement of a single file ID with another file OF IDENTICAL SIZE. Attempts to change the filesize will break the bundle.
    >CLmanglehmaps.py replace c:\Games\CardLife\Assets\bundles\terrain_bundle\ ac7156e0-7b70-4b48-bba0-cbd6f6f0c249 raw\heightmap.raw
    Just replaced heightmap.raw section with heightmap.raw file.