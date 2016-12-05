var common_width = 600;
var common_height = 200;

d3.json('data/fake_users1.json', function(data) {
    MG.data_graphic({
        title: "Line Chart #1",
        description: "This is a simple line chart.",
        data: MG.convert.date(data, 'date'),
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#4D4D4D',
        target: '#fake_users1',
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #2",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#5DA5DA',
        target: document.getElementById('fake_users2'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #3",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#FAA43A',
        target: document.getElementById('fake_users3'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #4",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#60BD68',
        target: document.getElementById('fake_users4'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #5",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#F17CB0',
        target: document.getElementById('fake_users5'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #6",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#B2912F',
        target: document.getElementById('fake_users6'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #6",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#B276B2',
        target: document.getElementById('fake_users7'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #6",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#DECF3F',
        target: document.getElementById('fake_users8'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #6",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#F15854',
        target: document.getElementById('fake_users9'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});

d3.json('data/fake_users1.json', function(data) {
    data = MG.convert.date(data, 'date');
    MG.data_graphic({
        title: "Line Chart #6",
        description: "This is a simple line chart.",
        data: data,
        width: common_width,
        height: common_height,
        right: 40,
        // color: '#8C001A',
        target: document.getElementById('fake_users10'),
        x_accessor: 'date',
        y_accessor: 'value'
    });
});
