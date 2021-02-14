SELECT smsoutbox.id AS outbox_id,
       smsinbox.id AS inbox_id,
       smsoutbox.learner_id,
       learners.phone_number,
       projects.partner_id,
       partners.name AS partner_name,
       projects.id AS project_id,
       projects.project_name,
       program_variations.program_id,
       programs.program_code,
       programs.program_name,
       packages.variation_id,
       program_variations.variation_code,
       program_variations.variation_name,
       smsoutbox.package_id,
       smsoutbox.message_type,
       smsoutbox.object_id,
       smsoutbox.message_out,
       smsinbox.message_in,
       smsoutbox.sender,
       smsinbox.created_at
FROM smsinbox
         LEFT JOIN smsoutbox ON smsoutbox.link_id = smsinbox.id
         LEFT JOIN learners ON smsoutbox.learner_id = learners.learner_id
         LEFT JOIN objects ON objects.id = smsoutbox.object_id
         LEFT JOIN packages ON packages.id = smsoutbox.package_id
         LEFT JOIN program_variations ON packages.variation_id = program_variations.id
         LEFT JOIN programs ON programs.id = program_variations.program_id
         LEFT JOIN projects ON programs.project_id = projects.id
         LEFT JOIN partners ON projects.partner_id = partners.id
WHERE smsinbox.created_at >= '2020-09-01' and partners.name = "Mastercard Kenya"