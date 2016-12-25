var common_width = 600;
var common_height = 250;

d3.json('data/created-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of created issues/tasks per day",
        description: "The chart shows the number of created issues or tasks per day",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#created-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});

d3.json('data/closed-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of closed issues/tasks per day",
        description: "The chart shows the number of closed issues or tasks per day",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#closed-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});


d3.json('data/open-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of issues in Open state per day",
        description: "The chart shows the number of issues or tasks in Open state per day",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#open-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});

d3.json('data/in-progress-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of issues in 'In progress' state per day",
        description: "The chart shows the number of issues or tasks in 'In progress' state per day",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#in-progress-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});

d3.json('data/on-hold-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of issues in 'On hold' state per day",
        description: "The chart shows the number of issues or tasks in 'On hold' state per day",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#on-hold-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});

d3.json('data/resolved-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of issues in Resolved state per day",
        description: "The chart shows the number of issues or tasks in Resolved state per day",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#resolved-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});

d3.json('data/not-closed-issues.json', function(data) {
    MG.data_graphic({
        title: "The number of not closed issues per day",
        description: "The chart shows the number of issues or tasks which are not closed per day."
                    + " The issues are in state: Open, In Progress, Resolved, On Hold, etc",
        data: MG.convert.date(data, 'datetime', '%Y-%m-%d'),
        width: common_width,
        height: common_height,
        left: 40,
        right: 40,
        // color: '#4D4D4D',
        target: '#not-closed-issues',
        x_accessor: 'datetime',
        y_accessor: 'value'
    });
});
