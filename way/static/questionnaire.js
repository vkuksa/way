let choices = {
  plus: [
    {
      text: 'Very Inaccurate',
      score: 1
    },
    {
      text: 'Moderately Inaccurate',
      score: 2
    },
    {
      text: 'Neither Accurate Nor Inaccurate',
      score: 3
    },
    {
      text: 'Moderately Accurate',
      score: 4
    },
    {
      text: 'Very Accurate',
      score: 5
    }
  ],
  minus: [
    {
      text: 'Very Inaccurate',
      score: 5
    },
    {
      text: 'Moderately Inaccurate',
      score: 4
    },
    {
      text: 'Neither Accurate Nor Inaccurate',
      score: 3
    },
    {
      text: 'Moderately Accurate',
      score: 2
    },
    {
      text: 'Very Accurate',
      score: 1
    }
  ]
};

$(function() {
    function getAnswers(keyed, id) {
        const answers = [];

        choices[keyed].forEach( choice => {
            answers.push('<div class="container">')
            answers.push(
                ` <input class="radio-buttons " type="radio" name="${id}" value="${choice.score}">
                 <label for="${id}">${choice.text}</label><br>`
            );
            answers.push('</div>')
        });

        return answers.join("");
    }

    function getItems(position, itemsPerPage, inventory) {
        const pos = parseInt(position);
        const pp = parseInt(itemsPerPage);
        const next = pos + pp;
        const back = pos - pp;
        const previous = back !== 0

        return {
            next: () => {
                return {
                    items: inventory.slice(next, next + pp),
                    finished: inventory.length === next,
                    position: next
                }
            },
            back: () => {
              return {
                items: inventory.slice(back, pos),
                previous,
                position: back
              }
            },
            current: () => {
              return {
                items: inventory.slice(pos, next),
                previous
              }
            }
        }
    }

    function handleBack() {
        window.scrollTo(0, 0)
        const { previous, items, position } = getItems(state.position, state.itemsPerPage, state.inventory).back()
        setState({ items, position, next: true, previous, source: "handleBack" })
    }

    function handleSubmit() {
        window.scrollTo(0, 0)
        const {items, finished, position} = getItems(state.position, state.itemsPerPage, state.inventory).next();

        if(finished) {
            handleFinish();
        } else {
            const next = items.filter(item => !state.answers[item.id]).length === 0;
            setState({ items, position, next, previous: true, source: "handleSubmit"})
        }
    }

    function handleStartup() {
        state.itemsPerPage = window.innerWidth < 600 ? 1 : 4
        const { items } = getItems(state.position, state.itemsPerPage, state.inventory).current()
        setState({ items, progress: 0, previous: false, next: false, source: "handleStartup" })
    }

    function handleFinish() {
        console.log("Submitting" + state.answers);
        const answers = state.answers;
        const choices = Object.keys(answers).reduce((prev, current) => {
            const choice = answers[current];
            prev.push({
              domain: choice.domain.domain,
              score: choice.score
            });
            return prev;
          }, []);

        $.ajax({
            type: "POST",
            url: "/test/" + test_id,
            contentType: "application/json",
            data: JSON.stringify(JSON.stringify(choices)),
            dataType: "json",
            success: function(response) {
                console.log(response);
            },
            error: function(err) {
                console.log(err);
            }
        });

        window.location.href = '/test/' + test_id + '/result';
    }

    function handleChange(id, value) {
        const { answers, items, inventory } = state
        const domain = inventory.find(q => q.id === id)
        answers[id] = { score: value, domain: domain}
        const progress = Math.round(Object.keys(answers).length / inventory.length * 100)
        const next = items.filter(item => !answers[item.id]).length === 0
        setState({ answers, progress, next, source: "handleChange" })
    }

    //Just make fucking state machine :)
    function setState({next, previous, items, position, answers, progress, source}={}) {
        console.log("Set state: " + next, previous, items, position, answers, progress, source);

        if(progress !== undefined) {
            state.progress = progress;
            $('.progress-bar').css('width', progress+'%').attr('aria-valuenow', progress);
        }
        if(position !== undefined) {
            state.position = position;
        }
        if(answers !== undefined) {
            state.answers = answers;
        }
        if(items !== undefined) {
            state.items = items;
            let output = [];
            output.push(`<section class="section-preview">`)

            items.forEach(
                (item) => {
                    let answers = getAnswers(item["keyed"], item.id);

                    output.push(`<div class="question-block row">
                        <div class="question container"> ${item.text} </div>
                        <div class="answer container"> ${answers} </div>
                      </div>`);
                }
            );

            output.push(`</section>`)
            $('#questionnaire-container').html(output.join(''));
        }

        $("#submit").prop('disabled', state.position === 116? true : next === false)
        $("#previous").prop('disabled', state.position === 0 ? true : previous === false)

        console.log("State: ", state);
    }

    $(document).on('change', ".radio-buttons", (function() {
        let obj = jQuery(this);
        handleChange(obj.attr('name'), obj.val())
    }))
    $(document).on('click', '#finish', function () {
        handleFinish()
    })
    $(document).on('click', '#previous', function () {
        handleBack()
    })
    $(document).on('click', '#submit', function () {
        handleSubmit()
    })

    $( document ).ready( function() {
        $.getJSON("/test/inventory",function(json){
            state.inventory = json;

            handleStartup();
        });
    });

    let state = {
        progress: 0,
        position: 0,
        inventory: [],
        itemsPerPage: 4,
        results: [],
        answers: [],
        items: []
    }
});