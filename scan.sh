#!/usr/bin/env sh


TMP_FILE=".offsets.txt"

function print_usage {
  cat <<EOF
Usage: scan [-i=image] [-r=regex] [-dhvV]
  -i=image: The raw disk image that should be scanned.
  -r=regex: The regex pattern that should be used.
  -d:       Run in dry mode.
  -h:       show help message.
  -v:       verbose output to stderr
  -V:       print version
EOF
}

function handle_arguments {
  for i in "$@"; do
    case $i in
      -i=*|--image=*)
        IMG="${i#*=}"
        shift # past argument=value
        ;;
      -r=*|--regex=*)
        REGEX="${i#*=}"
        shift # past argument=value
        ;;
      -d)
        DRYRUN=YES
        IMG="bachelor_os.img"
        REGEX="Max2017"
        TMP_FILE="Max2017_strings"
        shift
        ;;
      -v|--verbose)
        VERBOSE=YES
        shift # past argument with no value
        ;;
      -h|--help)
        print_usage
        exit 0
        ;;
      -*|--*)
        echo "Unknown option $i"
        exit 1
        ;;
      *)
        ;;
    esac
  done

  if [[ -z $DRYRUN ]]; then
    if [[ -z $IMG ]]; then
      echo "Error: Image option required."
      print_usage
      exit
    fi
    if [[ -z $REGEX ]]; then
      echo "Error: Pattern option required."
      print_usage
      exit
    fi
  fi
}

function get_offsets_using_grep {
  echo "Collecting offsets from '$IMG' for '$1' using grep"
  grep -a -o -b -iE $1 $IMG > $TMP_FILE

  # Adapt the greps output so we can spilt the file into columns
  sed -i 's/:/ /g' $TMP_FILE
}

function get_offsets_using_strings {
  echo "Collecting offsets from '$IMG' for '$1' using strings"
  strings -t d $IMG | grep -iE $1 > $TMP_FILE
}

function get_offset_info {
  echo "Offset:    $1"
  LINUX=1052672
  BLOCK="$((($1-($LINUX*512))/4096))"
  echo "Block:     $BLOCK"

  IS_ALLOCATED=$(blkstat -o $LINUX $IMG $BLOCK | head -n 2 | tail -n 1)
  echo "Status:    $IS_ALLOCATED"

  #INODE=$(ifind -o $LINUX -d $BLOCK $IMG)
  INODE=$(ifind -f ext -o $LINUX -d $BLOCK $IMG)
  echo "Inode:     $INODE"

  if [ "$INODE" = "Inode not found" ]; then
    return 0
  fi

  FILE_TYPE=$(icat -o $LINUX $IMG $INODE | file -)
  #FILE_TYPE=$(icat -o $LINUX $IMG $INODE | file - | grep -o -P '(?<=/dev/stdin: ).*?(?=,)')
  if [ "$FILE_TYPE" == *","* ]; then
    FILE_TYPE=$(echo $FILE_TYPE | awk -F":" '{print $2}' | sed -e 's/^[[:space:]]*//')
  else
    FILE_TYPE=$(echo $FILE_TYPE | awk -F"," '{print $1}' | awk -F":" '{print $2}' | sed -e 's/^[[:space:]]*//')
  fi
  echo "File Type: $FILE_TYPE"

  FILE_PATH=$(fls  -o $LINUX $IMG -rF | grep $INODE | awk -F":" '{print $2}' | sed -e 's/^[[:space:]]*//')
  echo "File Path: ${FILE_PATH}"
}

function main {
  handle_arguments "$@"

  if [[ -z $DRYRUN ]]; then
    get_offsets_using_grep $REGEX
  fi

  echo ""
  echo "Collecting informations from offsets:"
  echo "-------------------------------------"
  echo ""

  while read OFFSET rest; do
    get_offset_info $OFFSET
    echo ""
  done < "$TMP_FILE"

  # Delete tmp file
  if [[ -f "$TMP_FILE" ]]; then
      rm $TMP_FILE
  fi
}

main $@
#awk -F : "$awkfn"'BEGIN { get_offset_info() $1}' pas.txt
#awk '{"get_offset_info " $1}' pas.txt


#icat -o $LINUX $IMG $INODE > test.xlsx

