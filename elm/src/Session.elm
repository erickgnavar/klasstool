module Session exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode as Decode
import Json.Decode.Pipeline as Pipeline
import Json.Encode as Encode
import WebSocket


main : Program Flags Model Msg
main =
    Html.programWithFlags
        { init = init
        , update = update
        , view = view
        , subscriptions = subscriptions
        }



-- MODEL


type alias Flags =
    { websocket : String
    , sessionID : String
    }


type alias Model =
    { polls : List Poll
    , tmp : Maybe Poll
    , sessionID : String
    , websocket : String
    }


type alias Poll =
    { id : Int
    , title : String
    , finished : Bool
    , choices : List PollChoice
    , results : List PollResult
    , selectedChoice : Maybe PollChoice
    }


type alias PollResult =
    { value : String
    , votes : Int
    , percentage : Float
    , winner : Bool
    }


type alias PollChoice =
    { id : Int
    , value : String
    }


type alias PollResponse =
    { id : Int }



-- HTTP TYPES


type alias HttpPollResponse =
    { data : PollResponse
    }


type alias HttpPollList =
    { data : List Poll
    }


init : Flags -> ( Model, Cmd Msg )
init flags =
    ( { initModel | sessionID = flags.sessionID, websocket = flags.websocket }
    , fetchSession flags.sessionID
    )


samplePolls : List Poll
samplePolls =
    [ { id = 99
      , title = "my first poll"
      , choices =
            [ { value = "A", id = 1 }
            , { value = "B", id = 2 }
            , { value = "C", id = 3 }
            ]
      , results =
            [ { value = "Very interesting", votes = 20, percentage = 20, winner = False }
            , { value = "I dont know this shit", votes = 10, percentage = 1, winner = False }
            , { value = "lorem ipsum dolor something", votes = 75, percentage = 75, winner = False }
            , { value = "Value A", votes = 75, percentage = 10, winner = True }
            , { value = "Option B", votes = 75, percentage = 50, winner = False }
            ]
      , selectedChoice = Nothing
      , finished = False
      }
    ]


initModel : Model
initModel =
    { polls = []
    , tmp = Nothing
    , sessionID = ""
    , websocket = ""
    }


type Msg
    = Select Poll PollChoice
    | Vote Poll
    | PostResponse (Result Http.Error HttpPollResponse)
    | FetchPolls (Result Http.Error HttpPollList)
    | NewMessage String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Select poll choice ->
            ( selectPollChoice model poll (Just choice), Cmd.none )

        Vote poll ->
            let
                url =
                    "/api/v1/sessions/" ++ model.sessionID ++ "/responses/"

                body =
                    case poll.selectedChoice of
                        Just choice ->
                            Http.jsonBody <|
                                Encode.object
                                    [ ( "poll", Encode.int poll.id )
                                    , ( "choice", Encode.int choice.id )
                                    ]

                        Nothing ->
                            Http.emptyBody

                request =
                    Http.post url body httpPollResponseDecoder
            in
                ( model, Http.send PostResponse request )

        PostResponse (Ok response) ->
            ( model, Cmd.none )

        PostResponse (Err err) ->
            ( model, Cmd.none )

        FetchPolls (Ok response) ->
            ( { model | polls = (model.polls ++ response.data) }, Cmd.none )

        FetchPolls (Err err) ->
            ( model, Cmd.none )

        NewMessage str ->
            case Decode.decodeString pollDecoder str of
                Ok poll ->
                    ( insertOrReplacePoll model poll, Cmd.none )

                Err err ->
                    ( model, Cmd.none )


insertOrReplacePoll : Model -> Poll -> Model
insertOrReplacePoll model poll =
    --TODO: find why List.member does not work for this case
    if List.length (List.filter (\x -> x.id == poll.id) model.polls) == 1 then
        let
            newPolls =
                List.map
                    (\p ->
                        if p.id == poll.id then
                            poll
                        else
                            p
                    )
                    model.polls
        in
            { model | polls = newPolls }
    else
        { model | polls = poll :: model.polls }


selectPollChoice : Model -> Poll -> Maybe PollChoice -> Model
selectPollChoice model poll choice =
    let
        newPolls =
            List.map
                (\p ->
                    if p.id == poll.id then
                        { p | selectedChoice = choice }
                    else
                        p
                )
                model.polls
    in
        { model | polls = newPolls }



-- VIEW


choiceView : Poll -> PollChoice -> Html Msg
choiceView poll choice =
    div []
        [ input
            [ type_ "radio"
            , name "choice"
            , onClick (Select poll choice)
            ]
            []
        , text choice.value
        ]


resultView : PollResult -> Html Msg
resultView result =
    div
        [ class "result"
        ]
        [ span
            [ class
                ("result-fill "
                    ++ (if result.winner then
                            "result-fill-winner"
                        else
                            ""
                       )
                )
            , style
                [ ( "width", (toString result.percentage) ++ "%" )
                ]
            ]
            []
        , span
            [ class "result-content"
            ]
            [ b [] [ text ((toString result.percentage) ++ "%  ") ]
            , text result.value
            ]
        ]


disableButtonWithNoPollChoice : Maybe PollChoice -> Bool
disableButtonWithNoPollChoice selectedChoice =
    case selectedChoice of
        Just choice ->
            False

        Nothing ->
            True


activePollView : Poll -> Html Msg
activePollView poll =
    div []
        [ poll.choices
            |> List.map (choiceView poll)
            |> div []
        , button
            [ onClick (Vote poll)
            , class "btn btn-primary"
            , disabled (disableButtonWithNoPollChoice poll.selectedChoice)
            ]
            [ text "Vote" ]
        ]


finishedPollView : Poll -> Html Msg
finishedPollView poll =
    poll.results
        |> List.map resultView
        |> div []


pollView : Poll -> Html Msg
pollView poll =
    div [ class "poll-box" ]
        [ h1 []
            [ text poll.title ]
        , if poll.finished then
            finishedPollView poll
          else
            activePollView poll
        ]


view : Model -> Html Msg
view model =
    model.polls
        |> List.map pollView
        |> div []



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    WebSocket.listen model.websocket NewMessage


fetchSession : String -> Cmd Msg
fetchSession sessionID =
    let
        url =
            "/api/v1/sessions/" ++ sessionID ++ "/polls/"

        request =
            Http.get url httpPollListDecoder
    in
        Http.send FetchPolls request



-- DECODERS


httpPollListDecoder : Decode.Decoder HttpPollList
httpPollListDecoder =
    Pipeline.decode HttpPollList
        |> Pipeline.required "data" (Decode.list pollDecoder)


httpPollResponseDecoder : Decode.Decoder HttpPollResponse
httpPollResponseDecoder =
    Pipeline.decode HttpPollResponse
        |> Pipeline.required "data" pollResponseDecoder


pollDecoder : Decode.Decoder Poll
pollDecoder =
    Pipeline.decode Poll
        |> Pipeline.required "id" Decode.int
        |> Pipeline.required "title" Decode.string
        |> Pipeline.required "finished" Decode.bool
        |> Pipeline.required "choices" (Decode.list pollChoiceDecoder)
        |> Pipeline.required "results" (Decode.list pollResultDecoder)
        |> Pipeline.optional "selectedChoice" (Decode.maybe pollChoiceDecoder) Nothing


pollChoiceDecoder : Decode.Decoder PollChoice
pollChoiceDecoder =
    Pipeline.decode PollChoice
        |> Pipeline.required "id" Decode.int
        |> Pipeline.required "value" Decode.string


pollResponseDecoder : Decode.Decoder PollResponse
pollResponseDecoder =
    Pipeline.decode PollResponse
        |> Pipeline.required "id" Decode.int


pollResultDecoder : Decode.Decoder PollResult
pollResultDecoder =
    Pipeline.decode PollResult
        |> Pipeline.required "value" Decode.string
        |> Pipeline.required "votes" Decode.int
        |> Pipeline.required "percentage" Decode.float
        |> Pipeline.required "winner" Decode.bool
