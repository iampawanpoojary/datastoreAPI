set -euo pipefail

source util.sh

main() {
  # Get our working project, or exit if it's not set.
  local project_id=$(get_project_id)
  if [[ -z "$project_id" ]]; then
    exit 1
  fi
  local temp_file=$(mktemp)
  export TEMP_FILE="${temp_file}.json"
  mv "$temp_file" "$TEMP_FILE"
  < "$API_FILE" sed -E "s/YOUR-PROJECT-ID/${project_id}/g" > "$TEMP_FILE"
  echo "Deploying $API_FILE..."
  echo "gcloud endpoints services deploy $API_FILE"
  gcloud endpoints services deploy "$TEMP_FILE"
}

cleanup() {
  rm "$TEMP_FILE"
}

# Defaults.
API_FILE="mydatastorev1openapi.json"

if [[ "$#" == 0 ]]; then
  : # Use defaults.
elif [[ "$#" == 1 ]]; then
  API_FILE="$1"
else
  echo "Wrong number of arguments specified."
  exit 1
fi

trap cleanup EXIT

main "$@"
