#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
. "$DIR"/../integration-messages.sh

set -euxo pipefail

suite_started FW UPDATE
"$DIR"/vagrant-up.sh

cleanup() {
    suite_finished FW UPDATE
}
trap cleanup 0

test_with_command "FW_autofill" \
    vagrant ssh -c \"sudo /test/fw/FW_autofill.sh\"

test_with_command "FW_with_params_no_date" \
  vagrant ssh -c \"sudo /test/fw/FW_with_params_no_date.sh\"
