var GLOBALS = {
    jobs: [],
    annotators: {},
    reports: {},
    inputExamples: {}
}

function submit () {
    let fd = new FormData();
    var textInputElem = $('#input-text');
    var textVal = textInputElem.val();
    let inputFile = null;
    if (textVal.length > 0) {
        var textBlob = new Blob([textVal], {type:'text/plain'})
        inputFile = new File([textBlob], 'input');
    } else {
        var fileInputElem = $('#input-file')[0];
        if (fileInputElem.files.length > 0) {
            inputFile = fileInputElem.files[0];
        }
    }
    if (inputFile == null) {
        alert('Choose a input variants file, enter variants, or click an input example button.');
        return;
    }
    fd.append('file', inputFile);
    var submitOpts = {
        annotators: [],
        reports: []
    }
    var annotChecks = $('#annotator-select-div')
                        .find('.checkbox-group-check');
    for (var i = 0; i<annotChecks.length; i++){
        var cb = annotChecks[i];
        if (cb.checked) {
            submitOpts.annotators.push(cb.value);
        }
    }
    var reportChecks = $('#report-select-div')
                         .find('.checkbox-group-check');
    for (var i = 0; i<reportChecks.length; i++){
        var cb = reportChecks[i];
        if (cb.checked) {
            submitOpts.reports.push(cb.value);
        }
    }
    submitOpts.assembly = $('#assembly-select').val();
    var note = document.getElementById('jobnoteinput').value;
    submitOpts.note = note;
    fd.append('options',JSON.stringify(submitOpts));
    $.ajax({
        url:'submit',
        data: fd,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function (data) {
            addJob(data);
            buildJobsTable();
        }
    })
};

function addJob (jsonObj) {
    var trueDate = new Date(jsonObj.submission_time);
    jsonObj.submission_time = trueDate;
    GLOBALS.jobs.push(jsonObj);
    GLOBALS.jobs.sort((a, b) => {
        return b.submission_time.getTime() - a.submission_time.getTime();
    })

}

function createJobExcelReport (evt) {
    var jobid = evt.target.getAttribute('jobId');
    generateReport(jobid, 'excel', function () {
        populateJobs().then(function () {
            setTimeout(function () {
                buildJobsTable();
            }, 500);
        });
    });
}

function createJobTextReport (evt) {
    var jobid = evt.target.getAttribute('jobId');
    generateReport(jobid, 'text', function () {
        populateJobs().then(function () {
            setTimeout(function () {
                buildJobsTable();
            }, 500);
        });
    });
}

function buildJobsTable () {
    var allJobs = GLOBALS.jobs;
    var reportSelectors = $('.report-type-selector');
    var curSelectedReports = {};
    for (let i=0; i<reportSelectors.length; i++) {
        var selector = $(reportSelectors[i]);
        var jobId = selector.attr('jobId');
        var val = selector.val();
        curSelectedReports[jobId] = val;
    }
    $('.job-table-row').remove();
    var jobsTable = $('#jobs-table tbody');
    for (let i = 0; i < allJobs.length; i++) {
        job = allJobs[i];
        var jobTr = $(getEl('tr'))
            .addClass('job-table-row');
        jobsTable.append(jobTr);
        // Input file
        jobTr.append($(getEl('td')).append(job.orig_input_fname));
        // Job ID
        jobTr.append($(getEl('td')).append(job.id));
        // Status
        jobTr.append($(getEl('td')).append(job.status.status));
        // Note
        jobTr.append($(getEl('td')).append(job.note));
        /*
        // Submission time
        jobTr.append($(getEl('td')).append(job.submission_time.toLocaleString()));
        */
        // View
        var viewTd = $(getEl('td'));
        viewTd.css('text-align', 'center');
        jobTr.append(viewTd);
        var viewBtn = $(getEl('button')).append('Launch')
            .attr('disabled', !job.viewable)
            .attr('jobId', job.id)
            .click(jobViewButtonHandler);
        viewTd.append(viewBtn);
        // Database
        var dbTd = $(getEl('td'));
        dbTd.css('text-align', 'center');
        jobTr.append(dbTd);
        var dbButton = $(getEl('button'))
            .append('DB')
            .attr('jobId',job.id)
            .attr('disabled',!job.viewable)
            .click(jobDbDownloadButtonHandler);
        dbTd.append(dbButton);
        // Excel
        jobTr.append(dbTd);
        var dbButton = $(getEl('button'))
            .append('Excel')
            .attr('jobId',job.id)
        if (job.reports.includes('excel') == false) {
            dbButton.css('background-color', 'red');
            dbButton.click(createJobExcelReport);
        } else {
            dbButton.click(jobExcelDownloadButtonHandler);
        }
        dbTd.append(dbButton);
        // Text
        jobTr.append(dbTd);
        var dbButton = $(getEl('button'))
            .append('Text')
            .attr('jobId',job.id)
        if (job.reports.includes('text') == false) {
            dbButton.css('background-color', 'red');
            dbButton.click(createJobTextReport);
        } else {
            dbButton.click(jobTextDownloadButtonHandler);
        }
        dbTd.append(dbButton);
        /*
        // Reports
        var reportTd = $(getEl('td'));
        jobTr.append(reportTd);
        var reportSelector = $(getEl('select'))
            .attr('jobId',job.id)
            .addClass('report-type-selector')
            .change(reportSelectorChangeHandler)
        reportTd.append(reportSelector);
        jobReports = job.reports;
        let firstExistingReport;
        var curSelectedReport = curSelectedReports[job.id];
        for (let i=0; i<GLOBALS.reports.valid.length; i++) {
            let reportType = GLOBALS.reports.valid[i];
            if (firstExistingReport === undefined && jobReports.includes(reportType)) {
                firstExistingReport = reportType;
            }
            let typeOpt = $(getEl('option'))
            .attr('value', reportType)
            .append(reportType[0].toUpperCase()+reportType.slice(1));
            reportSelector.append(typeOpt);
        }
        var shownReportType = curSelectedReport ? curSelectedReport : firstExistingReport;
        reportSelector.val(shownReportType);
        var repDwnBtn = $(getEl('button'))
            .addClass('report-download-button')
            .append('Download')
            .attr('disabled', !job.reports.includes(shownReportType))
            .click(reportDownloadButtonHandler);
        reportTd.append(repDwnBtn);
        repGenBtn = $(getEl('button'))
            .append('Generate')
            .click(reportGenerateButtonHandler)
        reportTd.append(repGenBtn);
        */
        // Delete
        var deleteTd = $(getEl('td'));
        deleteTd.css('text-align', 'center');
        jobTr.append(deleteTd);
        var deleteBtn = $(getEl('button')).append('X');
        deleteTd.append(deleteBtn);
        deleteBtn.attr('jobId', job.id);
        deleteBtn.click(jobDeleteButtonHandler);
    }
}

function reportSelectorChangeHandler (event) {
    var selector = $(event.target);
    var downloadBtn = selector.siblings('.report-download-button');
    var jobId = selector.attr('jobId');
    var reportType = selector.val();
    let job;
    for (let i=0; i<GLOBALS.jobs.length; i++) {
        if (GLOBALS.jobs[i].id === jobId) {
            job = GLOBALS.jobs[i];
            break;
        }
    }
    downloadBtn.attr('disabled',!job.reports.includes(reportType));
}

function reportDownloadButtonHandler (event) {
    var btn = $(event.target);
    var selector = btn.siblings('.report-type-selector');
    var jobId = selector.attr('jobId');
    var reportType = selector.val();
    downloadReport(jobId, reportType);
}

function downloadReport (jobId, reportType) {
    // url = 'http://'+window.location.host+'/rest/jobs/'+jobId+'/reports/'+reportType;
    url = 'jobs/'+jobId+'/reports/'+reportType;
    downloadFile(url);
}

function generateReport (jobId, reportType, callback) {
    $.ajax({
        url:'jobs/'+jobId+'/reports/'+reportType,
        type: 'POST',
        processData: false,
        contentType: 'application/json',
        success: function (data) {
            callback();
        }
    })
}

function jobDbDownloadButtonHandler (event) {
    downloadJobDb($(event.target).attr('jobId'));
}

function jobExcelDownloadButtonHandler (event) {
    downloadJobExcel($(event.target).attr('jobId'));
}

function jobTextDownloadButtonHandler (event) {
    downloadJobText($(event.target).attr('jobId'));
}

function downloadJobDb (jobId) {
    url = 'jobs/'+jobId+'/db';
    downloadFile(url);
}

function downloadJobExcel (jobId) {
    url = 'jobs/'+jobId+'/excel';
    downloadFile(url);
}

function downloadJobText (jobId) {
    url = 'jobs/'+jobId+'/text';
    downloadFile(url);
}

function downloadFile (url) {
    $('#download-area').attr('src', url);
}

function getEl (tag) {
    return document.createElement(tag);
}

function jobViewButtonHandler (event) {
    var jobId = $(event.target).attr('jobId');
    let dbPath;
    var jobs = GLOBALS.jobs;
    for (let i=0; i<jobs.length; i++) {
        job = jobs[i];
        if (job.id === jobId) {
            dbPath = job.db_path;
            break;
        }
    }
    url = '/result/index.html?dbpath='+dbPath+'&job_id='+jobId;
    var win = window.open(url, '_blank');
    win.focus()
}

function jobDeleteButtonHandler (event) {
    var jobId = $(event.target).attr('jobId');
    deleteJob(jobId);
}

function deleteJob (jobId) {
    $.ajax({
        url:'jobs/'+jobId,
        type: 'DELETE',
        contentType: 'application/json',
        success: function (data) {
            populateJobs().then(() => {
                buildJobsTable();
            });
        }
    })
}

function addListeners () {
    $('#submit-job-button').click(submit);
    $('#input-text').change(inputChangeHandler);
    $('#input-file').change(inputChangeHandler);
    $('#all-annotators-button').click(allNoAnnotatorsHandler);
    $('#no-annotators-button').click(allNoAnnotatorsHandler);
    $('.input-example-button').click(inputExampleChangeHandler)
    $('#refresh-jobs-table-btn').click(refreshJobsTable);
    $('.jobsdirinput').change(setJobsDir);
}

function inputExampleChangeHandler (event) {
    var elem = $(event.target);
    var val = elem.val();
    var getExampleText = new Promise((resolve, reject) => {
        var cachedText = GLOBALS.inputExamples[val];
        if (cachedText === undefined) {
            var fname = val+'.txt'
            $.ajax({
                url:'input-examples/'+fname,
                type: 'GET',
                contentType: 'application/json',
                success: function (data) {
                    GLOBALS.inputExamples[val] = data;
                    resolve(data);
                }
            })
        } else {
            resolve(cachedText);
        }
    });
    getExampleText.then((text) => {
        var inputArea = $('#input-text');
        inputArea.val(text);
        inputArea.change();
    })
}

function allNoAnnotatorsHandler (event) {
    var elem = $(event.target);
    let checked;
    if (elem.attr('id') === 'all-annotators-button') {
        checked = true;
    } else {
        checked = false;
    }
    var annotCheckBoxes = $('.annotator-checkbox');
    for (var i = 0; i<annotCheckBoxes.length; i++){
        var cb = annotCheckBoxes[i];
        cb.checked = checked;
    }
}

function inputChangeHandler (event) {
    var target = $(event.target);
    var id = target.attr('id');
    if (id === 'input-file') {
        $('#input-text').val('');
    } else if (id === 'input-text') {
        var elem = $("#input-file");
        elem.wrap('<form>').closest('form').get(0).reset();
        elem.unwrap();
    }
}

var JOB_IDS = []

function populateJobs () {
    return new Promise((resolve, reject) => {
        $.ajax({
            url:'jobs',
            type: 'GET',
            success: function (allJobs) {
                GLOBALS.jobs = [];
                for (var i=0; i<allJobs.length; i++) {
                    let job = allJobs[i];
                    addJob(job);
                }
                resolve();
            }
        })
    });
}

function refreshJobsTable () {
    populateJobs().then(buildJobsTable());
}

function populateAnnotators () {
    return new Promise((resolve, reject) => {
        $.ajax({
            url:'annotators',
            type: 'GET',
            success: function (data) {
                GLOBALS.annotators = data
                resolve();
            }
        })
    });
}

function buildAnnotatorsSelector () {
    var annotCheckDiv = document.getElementById('annotator-select-div');
    let annotators = GLOBALS.annotators;
    let annotInfos = Object.values(annotators);
    // Sort by title
    annotInfos.sort((a,b) => {
        var x = a.title.toLowerCase();
        var y = b.title.toLowerCase();
        if (x < y) {return -1;}
        if (x > y) {return 1;}
        return 0;
    });
    let checkDatas = [];
    for (let i=0; i<annotInfos.length; i++) {
        var annotInfo = annotInfos[i];
        checkDatas.push({
            name: annotInfo.name,
            value: annotInfo.name,
            label: annotInfo.title,
            checked: true
        })
    }
    buildCheckBoxGroup(checkDatas, annotCheckDiv);
}

function buildCheckBoxGroup (checkDatas, parentDiv) {
    parentDiv = (parentDiv === undefined) ? getEl('div') : parentDiv;
    emptyElement(parentDiv);
    parentDiv.className = 'checkbox-group';
    // all-none buttons
    var allNoneDiv = getEl('div');
    addEl(parentDiv, allNoneDiv);
    allNoneDiv.className = 'checkbox-group-all-none-div';
    var parentId = parentDiv.id;
    if (parentId != 'report-select-div') {
        // all button
        allButton = getEl('button');
        addEl(allNoneDiv, allButton);
        allButton.className = 'checkbox-group-all-button';
        allButton.textContent = 'All';
        allButton.addEventListener('click', function (evt) {checkBoxGroupAllNoneHandler (evt);});
        // none button
        noneButton = getEl('button');
        addEl(allNoneDiv, noneButton);
        noneButton.className = 'checkbox-group-none-button';
        noneButton.textContent = 'None';
        noneButton.addEventListener('click', function (evt) {checkBoxGroupAllNoneHandler (evt);});
    }
    // flexbox
    var flexbox = getEl('div');
    addEl(parentDiv, flexbox);
    //flexbox.addClass('checkbox-group-flexbox');
    var checkDivs = [];
    // checks
    for (let i=0; i<checkDatas.length; i++) {
        var checkData = checkDatas[i];
        var checkDiv = getEl('div');
        addEl(flexbox, checkDiv);
        var check = getEl('input');
        check.className = 'checkbox-group-check';
        check.setAttribute('type', 'checkbox');
        check.setAttribute('name', checkData.name);
        check.setAttribute('value', checkData.value);
        check.setAttribute('checked', checkData.check);
        addEl(checkDiv, check);
        var label = getEl('span');
        label.style.fontFamily = 'monospace';
        label.style.fontSize = '16px';
        label.textContent = checkData.label;
        addEl(checkDiv, label);
        if (parentId != 'report-select-div') {
            var question = getEl('button');
            question.className = 'moduledetailbutton';
            question.textContent = '?';
            question.setAttribute('module', checkData.value);
            question.addEventListener('click', function (evt) {
                var annotchoosediv = document.getElementById('annotchoosediv');
                var moduledetaildiv = document.getElementById('moduledetaildiv_submit');
                if (moduledetaildiv != null) {
                    annotchoosediv.removeChild(moduledetaildiv);
                }
                var detaildiv = getModuleDetailDiv(evt.target.getAttribute('module'));
                addEl(annotchoosediv, detaildiv);
            });
            addEl(checkDiv, question);
        } else {
            checkDiv.style.display = 'inline-block';
        }
        checkDivs.push(checkDiv);
    }
    // resize all to match max
    /*
    var maxWidth = Math.max.apply(null, checkDivs.map(elem => elem.width()));
    for (let i=0; i<checkDivs.length; i++) {
        let checkDiv = checkDivs[i];
        checkDiv.width(maxWidth);
    }
    */
    return parentDiv;
}

function checkBoxGroupAllNoneHandler (event) {
    var elem = $(event.target);
    let checked;
    if (elem.hasClass('checkbox-group-all-button')) {
        checked = true;
    } else {
        checked = false;
    }
    var checkElems = elem.closest('.checkbox-group')
                           .find('input.checkbox-group-check');
    for (var i = 0; i<checkElems.length; i++){
        var checkElem = checkElems[i];
        checkElem.checked = checked;
    }
}

function populateReports () {
    return new Promise((resolve, reject) => {
        $.ajax({
            url:'reports',
            type: 'GET',
            success: function (data) {
                GLOBALS.reports = data
                resolve();
            }
        })
    })
}

function buildReportSelector () {
    var validReports = GLOBALS.reports.valid;
    var checkData = [];
    for (var i=0; i<validReports.length; i++) {
        reportName = validReports[i];
        checkData.push({
            name: reportName,
            value: reportName,
            label: reportName[0].toUpperCase()+reportName.slice(1),
            checked: reportName === GLOBALS.reports.default
        })
    }
    var reportDiv = document.getElementById('report-select-div');
    buildCheckBoxGroup(checkData, reportDiv);
}

function onTabChange () {
    var submitcontentdiv = document.getElementById('submitcontentdiv');
    var jobdiv = document.getElementById('jobdiv');
    var tab = document.getElementById('tabselect').selectedIndex;
    if (tab == 0) {
        submitcontentdiv.style.display = 'block';
        jobdiv.style.display = 'none';
    } else if (tab == 1) {
        submitcontentdiv.style.display = 'none';
        jobdiv.style.display = 'block';
    }
}

function getJobsDir () {
    $.get('/submit/getjobsdir').done(function (response) {
        $('.jobsdirtext').text(response);
    });
}

function setJobsDir (evt) {
    var d = evt.target.value;
    $.get('/submit/setjobsdir', {'jobsdir': d}).done(function (response) {
        $('.jobsdirtext').text(response);
        var promise = populateJobs();
        promise.then(function (response) {
            buildJobsTable();
        });
    });
}

function transitionToStore () {
    var submitdiv = document.getElementById('submitdiv');
    var storediv = document.getElementById('storediv');
    var settingsdiv = document.getElementById('settingsdiv');
    submitdiv.style.display = 'none';
    storediv.style.display = 'block';
    settingsdiv.style.display = 'none';
}

function transitionToSubmit () {
    var submitdiv = document.getElementById('submitdiv');
    var storediv = document.getElementById('storediv');
    var settingsdiv = document.getElementById('settingsdiv');
    submitdiv.style.display = 'block';
    storediv.style.display = 'none';
    settingsdiv.style.display = 'none';
}

function transitionToSettings () {
    var settingsdiv = document.getElementById('settingsdiv');
    var submitdiv = document.getElementById('submitdiv');
    var storediv = document.getElementById('storediv');
    submitdiv.style.display = 'none';
    storediv.style.display = 'none';
    settingsdiv.style.display = 'block';
}

function changePage (selectedPageId) {
    var pageselect = document.getElementById('pageselect');
    var pageIdDivs = pageselect.children;
    for (var i = 0; i < pageIdDivs.length; i++) {
        var pageIdDiv = pageIdDivs[i];
        var pageId = pageIdDiv.getAttribute('value');
        var page = document.getElementById(pageId);
        if (page.id == selectedPageId) {
            page.style.display = 'block';
            pageIdDiv.setAttribute('selval', 't');
        } else {
            page.style.display = 'none';
            pageIdDiv.setAttribute('selval', 'f');
        }
    }
}

function openSubmitDiv () {
    var div = document.getElementById('submitcontentdiv');
    div.style.display = 'block';
}

function loadSystemConf () {
    $.get('/submit/getsystemconfinfo').done(function (response) {
        var s = document.getElementById('sysconfpathspan');
        s.textContent = response['path'];
        var ta = document.getElementById('sysconftextarea');
        ta.value = response['content'];
    });
}

function updateSystemConf () {
    var data = {'sysconfstr': document.getElementById('sysconftextarea').value};
    $.ajax({
        url:'/submit/updatesystemconf',
        data: data,
        type: 'POST',
        success: function (response) {
            if (response['success'] == true) {
                alert('System configuration has been updated.');
            } else {
                alert('System configuration was not successful');
            }
            if (response['sysconf']['jobs_dir'] != undefined) {
                populateJobs().then(function () {
                    buildJobsTable();
                });
            }
        }
    });
}

function resetSystemConf () {
    $.get('/submit/resetsystemconf').done(function (response) {
        var status = response['status'];
        if (status == 'success') {
            var d = response['dict'];
            document.getElementById('sysconftextarea').value = d;
        } else {
            alert('Resetting system conf file failed.');
        }
    });
}

function showMd () {
    $.get('/store/getmd').done(function (response) {
        document.getElementById('modulesdirspan').textContent = response;
    });
}

function websubmit_run () {
    var md = showMd();
    var storediv = document.getElementById('storediv');
    storediv.style.display = 'none';
    connectWebSocket();
    getBaseModuleNames();
    getRemote();
    getLocal();
    document.addEventListener('click', function (evt) {
        if (evt.target.closest('#moduledetaildiv_submit') == null && evt.target.closest('.moduledetailbutton') == null ) {
            var div = document.getElementById('moduledetaildiv_submit');
            if (div != null) {
                div.style.display = 'none';
            }
        }
    });
    window.addEventListener('resize', function (evt) {
        var moduledetaildiv = document.getElementById('moduledetaildiv_submit');
        if (moduledetaildiv == null) {
            return;
        }
        var tdHeight = (window.innerHeight * 0.8 - 150) + 'px';
        var tds = document.getElementById('moduledetaildiv_submit').getElementsByTagName('table')[1].getElementsByTagName('td');
        tds[0].style.height = tdHeight;
        tds[1].style.height = tdHeight;
    });
    addListeners();
    jobsPromise = populateJobs();
    annotsPromise = populateAnnotators();
    reportsPromise = populateReports();
    Promise.all([jobsPromise, reportsPromise]).then(() => {
        buildJobsTable();
    })
    annotsPromise.then( () => {
        buildAnnotatorsSelector();
    })
    reportsPromise.then( () => {
        buildReportSelector();
    })
    getJobsDir();
    var submitcontentdiv = document.getElementById('submit-form');
    var h = window.innerHeight - 235;
    submitcontentdiv.style.height = h + 'px';
    loadSystemConf();
};

