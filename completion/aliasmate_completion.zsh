# compdef aliasmate
# requires yq for yaml and json parsing
_aliasmate() {
    local curcontext="$curcontext" state line aliases
    typeset -A opt_args

    local double_dash_count=0
    local word
    for word in "${words[@]}"; do
        [[ "$word" == '--' ]] && ((double_dash_count++))
    done

    # Define options
    local -a options
    options=(
        '-c[--configuration file]:config file:_files'
        '-s[--show-aliases]'
        '-v[--verbose]'
        '-h[--help]'
    )
    if (( double_dash_count == 1 )); then
        # After '--', you can define different completions if needed
       _arguments -C \
        '-c+[Specify config file]:config file:_files' \
        '*::argument:->aliases'
    else
        # No '--' in arguments
        # TODO: doesn't work after 2nd `--`
        # Provide options and aliases as completions
        _arguments -C \
            $options 
    fi

    case $state in
        aliases)
            if [[ -n "${opt_args[-c]}" ]]; then
                local config_file="${opt_args[-c]}"
                #echo $config_file
                if [[ -f "$config_file" ]]; then
                    aliases=(${(f)"$(yq -o y '.alias' "$config_file")"})
                    _describe 'alias' aliases
                    #echo $aliases
                    return
                fi
            fi
            ;;
    esac
}
compdef _aliasmate aliasmate
