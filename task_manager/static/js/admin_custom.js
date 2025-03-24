(function($) {
    $(document).ready(function() {
        $('input[name="is_active"]').change(
            function() {
                if (!confirm('Ви дійсно бажаєте змінити статус активності?')) {
                    $(this).prop('checked', !$(this).prop('checked'));
                }
            }
        );
    })
})