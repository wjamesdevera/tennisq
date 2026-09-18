"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import { useForm } from "react-hook-form";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import * as z from "zod";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

const CreateEventFormSchema = z.object({
  title: z.string().min(1, { message: "Title is required" }),
  description: z.string().optional(),
  date: z.string().min(1, { message: "Date is required" }),
  maxPlayers: z.coerce.number().int().positive().optional(),
});

type CreateEventFormInput = z.input<typeof CreateEventFormSchema>;
type CreateEventFormOutput = z.output<typeof CreateEventFormSchema>;

const CreateEventForm: React.FC = () => {
  const onSubmit = (data: CreateEventFormOutput) => {
    console.log(data);
  };

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateEventFormInput, undefined, CreateEventFormOutput>({
    resolver: zodResolver(CreateEventFormSchema),
  });
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col">
        <TextField
          label="Title"
          {...register("title")}
          error={!!errors.title}
          helperText={errors.title?.message}
        />
        <TextField
          label="Description"
          {...register("description")}
          error={!!errors.description}
          helperText={errors.description?.message}
        />

        <DatePicker label="Date" />
        {errors?.date && <p>{errors.date.message}</p>}

        <TextField
          label="Max Players"
          {...register("maxPlayers")}
          error={!!errors.maxPlayers}
          helperText={errors.maxPlayers?.message}
        />
        <Button variant="contained" type="submit">
          Create Event
        </Button>
      </form>
    </LocalizationProvider>
  );
};

export default CreateEventForm;
