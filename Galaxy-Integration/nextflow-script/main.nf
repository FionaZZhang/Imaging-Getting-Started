#!/usr/bin/env nextflow

process startWeb {
    script:
    """
    cd ../../../../
    cd galaxy-web
    npm run build
    cd ../backend
    python app.py &
    sleep 3
    open http://127.0.0.1:5000/
    """
}

workflow {

    startWeb()

}



